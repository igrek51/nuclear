import inspect
from typing import Dict, Mapping
from typing import Type, Any, List, TypeVar, Optional

from cliglue.args.args_que import ArgsQue
from cliglue.args.container import is_args_container_name, ArgsContainer
from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, KeywordRule, \
    DefaultActionRule, ValueRule, PositionalArgumentRule, AllArgumentsRule, SubcommandRule
from cliglue.builder.typedef import Action
from cliglue.parser.context import RunContext
from cliglue.parser.rule_process import normalize_keywords, TCliRule, filter_rules
from cliglue.utils.output import warn
from .error import CliDefinitionError, CliSyntaxError
from .keyword import names_from_keywords
from .param import match_param, parse_argument_value, parameter_display_name


class Parser(object):
    def __init__(self,
                 rules: List[CliRule],
                 run: Optional[Action] = None,
                 parent: Optional['Parser'] = None,
                 dry: bool = False,
                 subcommand: Optional[SubcommandRule] = None,
                 ):
        self.__run: Action = run
        self.__rules: List[CliRule] = rules
        self.__subcommand: SubcommandRule = subcommand
        self._init_rules()

        self.__parent: Optional['Parser'] = parent
        self.__action_triggered = parent.__action_triggered if parent else False
        self.__dry = dry

        self.__vars: Dict[str, Any] = dict()
        self._init_vars()

    def _init_rules(self):
        normalize_keywords(self._rules(FlagRule, ParameterRule))

        if not self.__run:
            rules: List[DefaultActionRule] = self._rules(DefaultActionRule)
            for rule in rules:
                self.__run = rule.run

        rules: List[ValueRule] = self._rules(ValueRule)
        for rule in rules:
            if rule.required and rule.default:
                raise CliDefinitionError('argument value may be either required or have the default value')

        pos_args = 0
        all_args = 0
        for rule in self._rules(PositionalArgumentRule, AllArgumentsRule):
            if isinstance(rule, PositionalArgumentRule):
                if all_args:
                    raise CliDefinitionError('positional argument can\'t be placed after all remaining arguments')
                pos_args += 1
            elif isinstance(rule, AllArgumentsRule):
                if all_args:
                    raise CliDefinitionError('all remaining arguments rule can be defined once')
                all_args += 1

    def _init_vars(self):
        for rule in self._rules(FlagRule):
            for name in names_from_keywords(rule.keywords):
                self.__vars[name] = False

        for rule in self._rules(ParameterRule):
            for name in names_from_keywords(rule.keywords):
                self.__vars[name] = rule.default

        for rule in self._rules(PositionalArgumentRule):
            self.__vars[rule.name] = rule.default

    def _rules(self, *types: Type[TCliRule]) -> List[TCliRule]:
        return filter_rules(self.__rules, *types)

    def parse_args(self, args_list: List[str]) -> Optional[RunContext]:
        args = ArgsQue(args_list)
        run_context: Optional[RunContext] = self._parse_args_queue(args)
        self._check_superfluous_args(args)
        return run_context

    def _parse_args_queue(self, args: ArgsQue) -> Optional[RunContext]:
        self._parse_flags(args)
        self._parse_params(args)
        deeper: Optional[RunContext] = self._parse_deeper(args)
        if deeper:
            return deeper
        self._parse_positional_arguments(args)
        self._parse_remaining_arguments(args)
        self._check_required_arguments()
        return self._run_default_action()

    def _parse_flags(self, args: ArgsQue):
        for arg in args:
            rule: FlagRule = self._find_rule(FlagRule, arg)
            if rule:
                args.pop_current()
                for name in names_from_keywords(rule.keywords):
                    self.__vars[name] = True

    def _parse_params(self, args: ArgsQue):
        for arg in args:
            for rule in self._rules(ParameterRule):
                value = match_param(rule, args, arg)
                if value:
                    self._parse_param(rule, value)

    def _parse_param(self, rule: ParameterRule, value_str: str):
        try:
            parsed_value = parse_argument_value(rule, value_str)
        except ValueError as e:
            param_name = parameter_display_name(rule)
            raise CliSyntaxError(f'parsing parameter "{param_name}"') from e
        if rule.name:
            self.__vars[rule.name] = parsed_value
        else:
            for name in names_from_keywords(rule.keywords):
                self.__vars[name] = parsed_value

    def _parse_deeper(self, args: ArgsQue) -> Optional[RunContext]:
        return self._parse_primary_oprions(args) or \
               self._parse_subcommand(args)

    def _parse_primary_oprions(self, args: ArgsQue) -> Optional[RunContext]:
        for arg in args:
            rule: PrimaryOptionRule = self._find_rule(PrimaryOptionRule, arg)
            if rule:
                args.pop_current()
                self.action_triggered = True
                subparser = Parser(rule.subrules, rule.run, parent=self)
                return subparser._parse_args_queue(args)

    def _parse_subcommand(self, args: ArgsQue) -> Optional[RunContext]:
        if args:
            # recognize first arg as a command
            first = next(iter(args))
            rule: SubcommandRule = self._find_rule(SubcommandRule, first)
            if rule:
                args.pop_current()
                subparser = Parser(rule.subrules, rule.run, parent=self, subcommand=rule)
                return subparser._parse_args_queue(args)

    def _parse_positional_arguments(self, args: ArgsQue):
        for arg, rule in zip(args.reset(), self._rules(PositionalArgumentRule)):
            self._parse_positional_argument(rule, args.pop_current())

    def _parse_positional_argument(self, rule: PositionalArgumentRule, arg: str):
        try:
            self.__vars[rule.name] = parse_argument_value(rule, arg)
        except ValueError as e:
            raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

    def _parse_remaining_arguments(self, args: ArgsQue):
        for rule in self._rules(AllArgumentsRule):
            remaining_args = args.pop_all()
            if rule.joined_with:
                value = rule.joined_with.join(remaining_args)
            else:
                value = remaining_args
            self.__vars[rule.name] = value

    def _run_default_action(self) -> Optional[RunContext]:
        if self.__run:
            return self._run_action(self.__run)
        elif self.__parent:
            return self.__parent._run_default_action()

    def _run_action(self, action: Action) -> RunContext:
        if action and not self.__dry:
            (args, _, _, _, _, _, annotations) = inspect.getfullargspec(action)
            if not args:
                action()
            else:
                kwargs = self._inject_args(args, annotations)
                action(**kwargs)
        return self._build_run_context(action)

    @staticmethod
    def _check_superfluous_args(args):
        if args:
            warn(f'unrecognized arguments: {" ".join(args)}')

    def _check_required_arguments(self):
        if self.__action_triggered:
            return

        for rule in self._rules(ParameterRule):
            if rule.required:
                for name in names_from_keywords(rule.keywords):
                    if not self.__vars[name]:
                        raise CliSyntaxError(f'required parameter "{", ".join(rule.keywords)}" is not given')

        for rule in self._rules(PositionalArgumentRule):
            if rule.required:
                if not self.__vars[rule.name]:
                    raise CliSyntaxError(f'required positional argument "{rule.name}" is not given')

        if self.__parent:
            self.__parent._check_required_arguments()

    TKeywordRule = TypeVar('TKeywordRule', bound=KeywordRule)

    def _find_rule(self, rule_type: Type[TKeywordRule], keyword: str) -> Optional[TKeywordRule]:
        for rule in self.__rules:
            if isinstance(rule, rule_type):
                if keyword in rule.keywords:
                    return rule

    def _inject_args(self, args: List[str], annotations: Mapping[str, Any]) -> Dict[str, Any]:
        return {arg: self._inject_arg(arg, annotations) for arg in args}

    def _inject_arg(self, arg: str, annotations: Mapping[str, Any]) -> Any:
        if arg in self.__vars:
            return self.__vars[arg]
        elif self.__parent:
            return self.__parent._inject_arg(arg, annotations)
        elif is_args_container_name(arg, annotations):
            return ArgsContainer(self.__vars)
        else:
            warn(f"can't inject argument '{arg}': name not found")
            return None

    def _build_run_context(self, action: Action) -> RunContext:
        args_container = ArgsContainer(self.__vars)
        active_subcommands = self._active_subcommands()
        active_rules = self._active_rules()
        return RunContext(args_container, action, active_subcommands, active_rules)

    def _active_subcommands(self) -> List[SubcommandRule]:
        subcommands: List[SubcommandRule] = []
        if self.__subcommand:
            subcommands.append(self.__subcommand)
        if self.__parent:
            return self.__parent._active_subcommands() + subcommands
        return subcommands

    def _active_rules(self) -> List[CliRule]:
        active_rules: List[CliRule] = self.__rules
        if self.__parent:
            active_rules.extend(self.__parent._active_rules())
        return active_rules
