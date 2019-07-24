from typing import Dict
from typing import Type, Any, List, TypeVar, Optional

from cliglue.args.args_que import ArgsQue
from cliglue.args.container import ArgsContainer
from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, KeywordRule, \
    DefaultActionRule, PositionalArgumentRule, ManyArgumentsRule, SubcommandRule, DictionaryRule, ValueRule
from cliglue.builder.typedef import Action
from cliglue.parser.flag import flag_default_value
from cliglue.parser.inject import run_action
from cliglue.utils.output import warn
from .choices import generate_value_choices
from .context import RunContext
from .dictionary import match_dictionary
from .error import CliSyntaxError
from .keyword import format_var_name
from .param import match_param, parameter_default_value
from .pos_arg import many_arguments_max_count, many_arguments_min_count
from .rule_process import normalize_keywords, TCliRule, filter_rules, \
    parse_rule_value, parse_typed_value
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
            for rule in self._rules(DefaultActionRule):
                self.__run = rule.run
        normalize_keywords(self._rules(FlagRule, ParameterRule, DictionaryRule))
        validate_rules(self.__rules)

    def _init_vars(self):
        for rule in self._rules(FlagRule):
            for keyword in rule.keywords:
                self._set_internal_var(keyword, flag_default_value(rule))

        for rule in self._rules(ParameterRule):
            for var_name in rule.var_names():
                self._set_internal_var(var_name, parameter_default_value(rule))

        for rule in self._rules(PositionalArgumentRule):
            self._set_internal_var(rule.name, rule.default)

        for rule in self._rules(ManyArgumentsRule):
            self._set_internal_var(rule.name, [])

        for rule in self._rules(DictionaryRule):
            for var_name in rule.var_names():
                self._set_internal_var(var_name, {})

    def _set_internal_var(self, var_name: str, value):
        self.__vars[format_var_name(var_name)] = value

    def _get_internal_var(self, var_name: str) -> Any:
        return self.__vars[format_var_name(var_name)]

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
            self._parse_dicts(args)
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
        self._check_strict_choices()
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
                oldval = self._get_internal_var(keyword)
                self._set_internal_var(keyword, oldval + 1)
            else:
                self._set_internal_var(keyword, True)

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
            parsed_value = parse_rule_value(rule, value_str)
        except ValueError as e:
            raise CliSyntaxError(f'parsing parameter "{rule.display_name()}"') from e

        self._set_param_value(rule, parsed_value)

    def _set_param_value(self, rule: ParameterRule, parsed_value):
        for var_name in rule.var_names():
            if rule.multiple:
                oldval: List = self._get_internal_var(var_name)
                oldval.append(parsed_value)
            else:
                self._set_internal_var(var_name, parsed_value)

    def _parse_dicts(self, args: ArgsQue):
        for arg in args:
            for rule in self._rules(DictionaryRule):
                raw_key, raw_value = match_dictionary(rule, args, arg)
                if raw_value:
                    entry_key = parse_typed_value(rule.key_type, raw_key)
                    entry_value = parse_typed_value(rule.value_type, raw_value)
                    self._add_dict_value(rule, entry_key, entry_value)

    def _add_dict_value(self, rule: DictionaryRule, entry_key, entry_value):
        for var_name in rule.var_names():
            oldval: Dict = self._get_internal_var(var_name)
            oldval[entry_key] = entry_value
            self._set_internal_var(var_name, oldval)

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
            self._set_internal_var(rule.name, parse_rule_value(rule, arg))
        except ValueError as e:
            raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

    def _parse_many_arguments(self, args: ArgsQue):
        args.reset()
        for rule in self._rules(ManyArgumentsRule):
            retrieve_count: Optional[int] = many_arguments_max_count(rule)
            if not retrieve_count:
                retrieve_count = len(args)

            if len(args) < retrieve_count:
                raise CliSyntaxError(f'{retrieve_count} positional arguments are required,'
                                     f' but "{len(args)} given"')

            retrieved = []
            for _ in range(retrieve_count):
                arg = args.pop_current()

                try:
                    parsed_value = parse_rule_value(rule, arg)
                    retrieved.append(parsed_value)
                except ValueError as e:
                    raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

            if rule.joined_with:
                var_value = rule.joined_with.join(retrieved)
            else:
                var_value = retrieved

            self._set_internal_var(rule.name, var_value)

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
        run_action(action, self._internal_vars_merged())
        return self._build_run_context(action)

    def _check_superfluous_args(self, args):
        if args and not self.__dry:
            warn(f'unrecognized arguments: {" ".join(args)}')

    def _check_required_arguments(self):
        if self.__dry:
            return

        for rule in self._rules(ParameterRule):
            if rule.required:
                for name in rule.var_names():
                    if not self._get_internal_var(name):
                        raise CliSyntaxError(f'required parameter "{", ".join(rule.keywords)}" is not given')

        for rule in self._rules(PositionalArgumentRule):
            if rule.required:
                if not self._get_internal_var(rule.name):
                    raise CliSyntaxError(f'required positional argument "{rule.name}" is not given')

        for rule in self._rules(ManyArgumentsRule):
            expected_count: Optional[int] = many_arguments_min_count(rule)
            if expected_count:
                given_count = len(self._get_internal_var(rule.name))
                if given_count != expected_count:
                    raise CliSyntaxError(f'"{expected_count}" arguments are required, but "{given_count}" were given')

        if self.__parent and not self.__action_triggered:
            self.__parent._check_required_arguments()

    def _check_strict_choices(self):
        if self.__dry:
            return

        for rule in self._rules(ValueRule):
            if rule.strict_choices and rule.choices:
                available_choices = generate_value_choices(rule)

                if isinstance(rule, ParameterRule):
                    for name in rule.var_names():
                        var_value = self._get_internal_var(name)
                        if var_value not in available_choices:
                            raise CliSyntaxError(f'parameter value {var_value} does not belong to available choices: '
                                                 f'{available_choices}')

                elif isinstance(rule, PositionalArgumentRule):
                    var_value = self._get_internal_var(rule.name)
                    if var_value not in available_choices:
                        raise CliSyntaxError(
                            f'positional argument value {var_value} does not belong to available choices: '
                            f'{available_choices}')

                elif isinstance(rule, ManyArgumentsRule):
                    var_values: List = self._get_internal_var(rule.name)
                    for var_value in var_values:
                        if var_value not in available_choices:
                            raise CliSyntaxError(
                                f'one of arguments value {var_value} does not belong to available choices: '
                                f'{available_choices}')

        if self.__parent and not self.__action_triggered:
            self.__parent._check_strict_choices()

    def _rules(self, *types: Type[TCliRule]) -> List[TCliRule]:
        return filter_rules(self.__rules, *types)

    TKeywordRule = TypeVar('TKeywordRule', bound=KeywordRule)

    def _find_rule(self, rule_type: Type[TKeywordRule], keyword: str) -> Optional[TKeywordRule]:
        for rule in self.__rules:
            if isinstance(rule, rule_type):
                if keyword in rule.keywords:
                    return rule

    def _internal_vars_merged(self) -> Dict[str, Any]:
        if self.__parent:
            return {**self.__parent._internal_vars_merged(), **self.__vars}
        return self.__vars

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
