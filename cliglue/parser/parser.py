import inspect
from typing import Dict, Mapping
from typing import Type, Any, List, TypeVar, Optional

from cliglue.args.args_que import ArgsQue
from cliglue.args.container import is_args_container_name, ArgsContainer
from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, KeywordRule, \
    DefaultActionRule, PositionalArgumentRule, ManyArgumentsRule, SubcommandRule, ValueRule
from cliglue.builder.typedef import Action
from cliglue.parser.context import RunContext
from cliglue.parser.rule_process import normalize_keywords, TCliRule, filter_rules, many_arguments_retrieve_count
from cliglue.utils.output import warn
from .error import CliSyntaxError
from .keyword import names_from_keywords, name_from_keyword
from .param import match_param, parse_argument_value, parameter_display_name
from .validate import validate_rules


class Parser(object):
    def __init__(self,
                 rules: List[CliRule],
                 run: Optional[Action] = None,
                 parent: Optional['Parser'] = None,
                 dry: bool = False,
                 subcommand: Optional[SubcommandRule] = None,
                 ):
        """
        Command line arguments parser
        :param rules: list of rules defined for the base level of parser
        :param run: default action to invoke when it's triggered
        :param parent: parent parser for sub-parser on the deeper level
        :param dry: whether dry run should be invoked. Dry run does not trigger any action.
        :param subcommand: A subcommand rule from which this parser is derived
        """
        self.__run: Action = run
        self.__rules: List[CliRule] = rules
        self.__subcommand: SubcommandRule = subcommand
        self._init_rules()

        self.__parent: Optional['Parser'] = parent
        self.__action_triggered = parent.__action_triggered if parent else False
        self.__dry = parent.__dry if parent else dry

        self.__vars: Dict[str, Any] = dict()
        self._init_vars()

    def _init_rules(self):
        if not self.__run:
            rules: List[DefaultActionRule] = self._rules(DefaultActionRule)
            for rule in rules:
                self.__run = rule.run
        normalize_keywords(self._rules(FlagRule, ParameterRule))
        validate_rules(self.__rules)

    def _init_vars(self):
        for rule in self._rules(FlagRule):
            for keyword in rule.keywords:
                if rule.multiple:
                    self._set_var(keyword, 0)
                else:
                    self._set_var(keyword, False)

        for rule in self._rules(ParameterRule):
            for keyword in rule.keywords:
                if rule.multiple:
                    if not rule.default:
                        default_value = []
                    elif not isinstance(rule.default, list):
                        default_value = [rule.default]
                    else:
                        default_value = rule.default
                    self._set_var(keyword, default_value)
                else:
                    self._set_var(keyword, rule.default)

        for rule in self._rules(PositionalArgumentRule):
            self._set_var(rule.name, rule.default)

        for rule in self._rules(ManyArgumentsRule):
            self._set_var(rule.name, [])

    def _set_var(self, name: str, value):
        self.__vars[name_from_keyword(name)] = value

    def _rules(self, *types: Type[TCliRule]) -> List[TCliRule]:
        return filter_rules(self.__rules, *types)

    def parse_args(self, args_list: List[str]) -> Optional[RunContext]:
        """
        Parse arguments list, read all flags, parameters and run triggered actions
        :param args_list:
        :return: run context containing all the details of triggered actions
        and particular state of parser (matched commands)
        """
        args = ArgsQue(args_list[:])
        run_context: Optional[RunContext] = self._parse_args_queue(args)
        self._check_superfluous_args(args)
        return run_context

    def _parse_args_queue(self, args: ArgsQue) -> Optional[RunContext]:
        try:
            self._parse_single_flags(args)
            self._parse_params(args)
            self._parse_combined_flags(args)
            return self._parse_primary_options(args) or \
                self._parse_subcommand(args) or \
                self._parse_current_level(args)
        except CliSyntaxError as e:
            if self.__dry:
                return self._build_run_context(None)
            else:
                raise e

    def _parse_current_level(self, args):
        self._parse_positional_arguments(args)
        self._parse_many_arguments(args)
        self._check_required_arguments()
        return self._run_default_action()

    def _parse_single_flags(self, args: ArgsQue):
        for arg in args:
            rule: FlagRule = self._find_rule(FlagRule, arg)
            if rule:
                args.pop_current()
                self._set_single_flag(rule)

    def _set_single_flag(self, rule: FlagRule):
        for keyword in rule.keywords:
            if rule.multiple:
                oldval = self.__vars[name_from_keyword(keyword)]
                self._set_var(keyword, oldval + 1)
            else:
                self._set_var(keyword, True)

    def _parse_combined_flags(self, args: ArgsQue):
        for arg in args:
            rules = self._extract_combined_flag(arg)
            if rules:
                args.pop_current()
                for rule in rules:
                    self._set_single_flag(rule)

    def _extract_combined_flag(self, arg: str) -> List[FlagRule]:
        if not arg.startswith('-') or arg.startswith('--'):
            return []
        matched_flags = []
        for single_char in arg[1:]:
            rule: FlagRule = self._find_rule(FlagRule, f'-{single_char}')
            if rule:
                matched_flags.append(rule)
            else:
                return []  # every combined character has to be detected as single flag
        return matched_flags

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
            self._set_param(rule, rule.name, parsed_value)
        else:
            for name in names_from_keywords(rule.keywords):
                self._set_param(rule, name, parsed_value)

    def _set_param(self, rule, name, parsed_value):
        if rule.multiple:
            oldval: List = self.__vars[name_from_keyword(name)]
            oldval.append(parsed_value)
        else:
            self._set_var(name, parsed_value)

    def _parse_primary_options(self, args: ArgsQue) -> Optional[RunContext]:
        for arg in args:
            rule: PrimaryOptionRule = self._find_rule(PrimaryOptionRule, arg)
            if rule:
                args.pop_current()
                self.__action_triggered = True
                subparser = Parser(rule.subrules, rule.run, parent=self)
                return subparser._parse_args_queue(args)

    def _parse_subcommand(self, args: ArgsQue) -> Optional[RunContext]:
        if args:
            # recognize first argument as a command
            first = args.reset().peek_current()
            rule: SubcommandRule = self._find_rule(SubcommandRule, first)
            if rule:
                args.pop_current()
                subparser = Parser(rule.subrules, rule.run, parent=self, subcommand=rule)
                return subparser._parse_args_queue(args)

    def _parse_positional_arguments(self, args: ArgsQue):
        for arg, rule in zip(args.reset(), self._rules(PositionalArgumentRule)):
            self._parse_positional_argument(rule, args.pop_current())

        if self.__parent and not self.__action_triggered:
            self.__parent._parse_positional_arguments(args)

    def _parse_positional_argument(self, rule: PositionalArgumentRule, arg: str):
        try:
            self._set_var(rule.name, parse_argument_value(rule, arg))
        except ValueError as e:
            raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

    def _parse_many_arguments(self, args: ArgsQue):
        args.reset()
        for rule in self._rules(ManyArgumentsRule):
            retrieve_count: Optional[int] = many_arguments_retrieve_count(rule)
            if not retrieve_count:
                retrieve_count = len(args)

            if len(args) < retrieve_count:
                raise CliSyntaxError(f'{retrieve_count} positional arguments are required,'
                                     f' but "{len(args)} given"')

            retrieved = []
            for _ in range(retrieve_count):
                arg = args.pop_current()

                try:
                    parsed_value = parse_argument_value(rule, arg)
                    retrieved.append(parsed_value)
                except ValueError as e:
                    raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

            if rule.joined_with:
                var_value = rule.joined_with.join(retrieved)
            else:
                var_value = retrieved

            self._set_var(rule.name, var_value)

        if self.__parent:
            self.__parent._parse_many_arguments(args)

    def _run_default_action(self) -> Optional[RunContext]:
        if self.__dry:
            return self._build_run_context(self.__run)
        if self.__run:
            return self._run_action(self.__run)
        elif self.__parent:
            return self.__parent._run_default_action()

    def _run_action(self, action: Action) -> RunContext:
        if action:
            (args, _, _, _, _, _, annotations) = inspect.getfullargspec(action)
            if not args:
                action()
            else:
                kwargs = self._inject_args(args, action, annotations)
                action(**kwargs)
        return self._build_run_context(action)

    def _check_superfluous_args(self, args):
        if args and not self.__dry:
            warn(f'unrecognized arguments: {" ".join(args)}')

    def _check_required_arguments(self):
        if self.__dry:
            return

        for rule in self._rules(ParameterRule):
            if rule.required:
                for name in names_from_keywords(rule.keywords):
                    if not self.__vars[name]:
                        raise CliSyntaxError(f'required parameter "{", ".join(rule.keywords)}" is not given')

        for rule in self._rules(PositionalArgumentRule):
            if rule.required:
                if not self.__vars[name_from_keyword(rule.name)]:
                    raise CliSyntaxError(f'required positional argument "{rule.name}" is not given')

        for rule in self._rules(ManyArgumentsRule):
            given_count = len(self.__vars[name_from_keyword(rule.name)])
            if rule.count:
                if given_count != rule.count:
                    raise CliSyntaxError(f'"{rule.count}" arguments are required, but "{given_count}" were given')
            if rule.min_count:
                if given_count < rule.min_count:
                    raise CliSyntaxError(f'"{rule.min_count}" or more arguments are required,'
                                         f' but only "{given_count}" were given')
            if rule.max_count:
                if given_count > rule.max_count:
                    raise CliSyntaxError(f'maximum "{rule.max_count}" arguments are required,'
                                         f' but "{given_count}" were given')

        if self.__parent and not self.__action_triggered:
            self.__parent._check_required_arguments()

    TKeywordRule = TypeVar('TKeywordRule', bound=KeywordRule)

    def _find_rule(self, rule_type: Type[TKeywordRule], keyword: str) -> Optional[TKeywordRule]:
        for rule in self.__rules:
            if isinstance(rule, rule_type):
                if keyword in rule.keywords:
                    return rule

    def _inject_args(self, args: List[str], action: Action, annotations: Mapping[str, Any]) -> Dict[str, Any]:
        return {arg: self._inject_arg(arg, action, annotations) for arg in args}

    def _inject_arg(self, arg: str, action: Action, annotations: Mapping[str, Any]) -> Any:
        if arg in self.__vars:
            return self.__vars[arg]
        elif self.__parent:
            return self.__parent._inject_arg(arg, action, annotations)
        elif is_args_container_name(arg, annotations):
            return ArgsContainer(self.__vars)
        else:
            warn(f"can't inject argument '{arg}' to function '{action.__name__}': name not found")
            return None

    def _build_run_context(self, action: Optional[Action]) -> RunContext:
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
        active_rules: List[CliRule] = self.__rules[:]
        if self.__parent:
            active_rules.extend(self.__parent._active_rules())
        return active_rules
