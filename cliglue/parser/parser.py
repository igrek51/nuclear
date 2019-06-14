import inspect
from typing import Dict, Mapping
from typing import Type, Any, List, TypeVar, Optional

from cliglue.args.args import is_args_container_name, ArgsContainer
from cliglue.args.args_que import ArgsQue
from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, ParentRule, KeywordRule, \
    DefaultActionRule, ValueRule, filter_rules, TCliRule, PositionalArgumentRule, AllArgumentsRule
from cliglue.builder.typedef import Action
from cliglue.utils.output import warn
from .error import CliDefinitionError, CliSyntaxError
from .keyword import names_from_keywords, keywords_from_names
from .param import match_param, parse_argument_value


class Parser(object):
    def __init__(self,
                 rules: List[CliRule],
                 run: Action,
                 parent: 'Parser' = None,
                 ):
        self.__run: Action = run
        self.__rules: List[CliRule] = rules
        self.init_rules()

        self.parent: Optional['Parser'] = parent

        self.vars: Dict[str, Any] = dict()
        self.init_vars()

    def init_rules(self):
        rules: List[KeywordRule] = self.rules(FlagRule, ParameterRule)
        for rule in rules:
            rule.keywords = keywords_from_names(set(rule.keywords))

        if not self.__run:
            rules: List[DefaultActionRule] = self.rules(DefaultActionRule)
            for rule in rules:
                self.__run = rule.run

        rules: List[ValueRule] = self.rules(ValueRule)
        for rule in rules:
            if rule.required and rule.default:
                raise CliDefinitionError('argument value may be either required or have the default value')

        pos_args = 0
        all_args = 0
        for rule in self.rules(PositionalArgumentRule, AllArgumentsRule):
            if isinstance(rule, PositionalArgumentRule):
                if all_args:
                    raise CliDefinitionError('positional argument can\'t be placed after all remaining arguments')
                pos_args += 1
            elif isinstance(rule, AllArgumentsRule):
                if all_args:
                    raise CliDefinitionError('all remaining arguments rule can be defined once')
                all_args += 1

    def init_vars(self):
        for rule in self.rules(FlagRule):
            for name in names_from_keywords(rule.keywords):
                self.vars[name] = False

        for rule in self.rules(ParameterRule):
            for name in names_from_keywords(rule.keywords):
                self.vars[name] = rule.default

        for rule in self.rules(PositionalArgumentRule):
            self.vars[rule.name] = rule.default

    def rules(self, *types: Type[TCliRule]) -> List[TCliRule]:
        return filter_rules(self.__rules, *types)

    def parse_args(self, args_list: List[str]):
        self._parse_args_queue(ArgsQue(args_list))

    def _parse_args_queue(self, args: ArgsQue):
        self._parse_flags(args)
        self._parse_params(args)
        if not self._parse_primary_options(args):
            if not self._parse_deeper(args):
                self._parse_positional_arguments(args)
                self._parse_remaining_arguments(args)
                self._run_default_action()
        self._check_superfluous_args(args)

    def _parse_flags(self, args: ArgsQue):
        for arg in args:
            rule: FlagRule = self._find_rule(FlagRule, arg)
            if rule:
                args.pop_current()
                for name in names_from_keywords(rule.keywords):
                    self.vars[name] = True

    def _parse_params(self, args: ArgsQue):
        for arg in args:
            for rule in self.rules(ParameterRule):
                value = match_param(rule, args, arg)
                if value:
                    self._parse_param(rule, value)

    def _parse_param(self, rule: ParameterRule, value_str: str):
        parsed_value = parse_argument_value(rule, value_str)
        if rule.name:
            self.vars[rule.name] = parsed_value
        else:
            for name in names_from_keywords(rule.keywords):
                self.vars[name] = parsed_value

    def _parse_primary_options(self, args: ArgsQue):
        for arg in args:
            rule: PrimaryOptionRule = self._find_rule(PrimaryOptionRule, arg)
            if rule:
                args.pop_current()
                self._run_action(rule.run)
                return True  # one primary option only
        return False

    def _parse_deeper(self, args: ArgsQue):
        if args:
            first = next(iter(args))
            # recognize first arg as command
            rule: ParentRule = self._find_rule(ParentRule, first)
            if rule:
                args.pop_current()
                # pass all remaining args to subparser
                subparser = Parser(rule.subrules, rule.run, parent=self)
                subparser._parse_args_queue(args)
                return True
        return False

    def _parse_positional_arguments(self, args: ArgsQue):
        for arg, rule in zip(args.reset(), self.rules(PositionalArgumentRule)):
            self._parse_positional_argument(rule, args.pop_current())

    def _parse_positional_argument(self, rule: PositionalArgumentRule, arg: str):
        self.vars[rule.name] = parse_argument_value(rule, arg)

    def _parse_remaining_arguments(self, args: ArgsQue):
        for rule in self.rules(AllArgumentsRule):
            remaining_args = args.pop_all()
            if rule.joined_with:
                value = rule.joined_with.join(remaining_args)
            else:
                value = remaining_args
            self.vars[rule.name] = value

    def _run_default_action(self):
        self._check_required_params()
        if self.__run:
            self._run_action(self.__run)
        elif self.parent:
            self.parent._run_default_action()

    def _run_action(self, action: Action):
        if action is not None:
            (args, _, _, _, _, _, annotations) = inspect.getfullargspec(action)
            if not args:
                action()
            else:
                kwargs = self._inject_args(args, annotations)
                action(**kwargs)

    @staticmethod
    def _check_superfluous_args(args):
        if args:
            warn('unrecognized arguments: {}'.format(' '.join(args)))

    def _check_required_params(self):
        for rule in self.rules(ParameterRule):
            if rule.required:
                for name in names_from_keywords(rule.keywords):
                    if not self.vars[name]:
                        raise CliSyntaxError('required parameter "{}" is not given'.format(', '.join(rule.keywords)))

        for rule in self.rules(PositionalArgumentRule):
            if rule.required:
                if not self.vars[rule.name]:
                    raise CliSyntaxError('required positional argument "{}" is not given'.format(rule.name))

        if self.parent:
            self.parent._check_required_params()

    TKeywordRule = TypeVar('TKeywordRule', bound=KeywordRule)

    def _find_rule(self, rule_type: Type[TKeywordRule], keyword: str) -> Optional[TKeywordRule]:
        for rule in self.__rules:
            if isinstance(rule, rule_type):
                if keyword in rule.keywords:
                    return rule

    def _inject_args(self, args: List[str], annotations: Mapping[str, Any]) -> Dict[str, Any]:
        return {arg: self._inject_arg(arg, annotations) for arg in args}

    def _inject_arg(self, arg: str, annotations: Mapping[str, Any]) -> Any:
        if arg in self.vars:
            return self.vars[arg]
        elif self.parent:
            return self.parent._inject_arg(arg, annotations)
        elif is_args_container_name(arg, annotations):
            return ArgsContainer(self.vars)
        else:
            warn("can't inject argument '{}': name not found".format(arg))
            return None
