from typing import Dict
from typing import Type, Any, List, TypeVar, Optional

from nuclear.args.args_que import ArgsQue
from nuclear.args.container import ArgsContainer
from nuclear.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, KeywordRule, \
    DefaultActionRule, PositionalArgumentRule, ManyArgumentsRule, SubcommandRule, DictionaryRule, ValueRule
from nuclear.builder.typedef import Action
from nuclear.sublog import log
from .context import RunContext
from .error import CliSyntaxError
from .inject import run_action
from .internal_vars import InternalVars
from .matcher import match_param, match_dictionary
from .transform import normalize_keywords, TCliRule, filter_rules
from .validate import validate_rules, check_strict_choices, check_required_arguments
from .value import parse_value_rule, parse_typed_value


class Parser(object):
    def __init__(self,
                 rules: List[CliRule],
                 run: Optional[Action] = None,
                 parent: Optional['Parser'] = None,
                 dry: bool = False,
                 subcommand: Optional[SubcommandRule] = None,
                 error_unrecognized: bool = False,
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
        self.__error_unrecognized = error_unrecognized

        self.internal_vars = InternalVars()
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
                self.internal_vars[keyword] = rule.default_value()

        for rule in self._rules(ParameterRule):
            for var_name in rule.var_names():
                self.internal_vars[var_name] = rule.default_value()

        for rule in self._rules(PositionalArgumentRule):
            self.internal_vars[rule.name] = rule.default

        for rule in self._rules(ManyArgumentsRule):
            self.internal_vars[rule.name] = []

        for rule in self._rules(DictionaryRule):
            for var_name in rule.var_names():
                self.internal_vars[var_name] = {}

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

        if run_context and run_context.action and not self.__dry:
            run_action(run_context.action, run_context.internal_vars)

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

    def _parse_current_level(self, args: ArgsQue) -> Optional[RunContext]:
        self._parse_positional_arguments(args)
        self._parse_many_arguments(args)
        if not self.__dry:
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
                oldval = self.internal_vars[keyword]
                self.internal_vars[keyword] = oldval + 1
            else:
                self.internal_vars[keyword] = True

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
            parsed_value = parse_value_rule(rule, value_str)
        except ValueError as e:
            raise CliSyntaxError(f'parsing parameter "{rule.display_name()}"') from e

        self._set_param_value(rule, parsed_value)

    def _set_param_value(self, rule: ParameterRule, parsed_value):
        for var_name in rule.var_names():
            if rule.multiple:
                oldval: List = self.internal_vars[var_name]
                oldval.append(parsed_value)
            else:
                self.internal_vars[var_name] = parsed_value

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
            oldval: Dict = self.internal_vars[var_name]
            oldval[entry_key] = entry_value
            self.internal_vars[var_name] = oldval

    def _parse_primary_options(self, args: ArgsQue) -> Optional[RunContext]:
        for arg in args:
            rule: PrimaryOptionRule = self._find_rule(PrimaryOptionRule, arg)
            if rule:
                args.pop_current()
                self.__action_triggered = True
                subparser = Parser(rule.subrules, rule.run, parent=self)
                return subparser._parse_args_queue(args)
        return None

    def _parse_subcommand(self, args: ArgsQue) -> Optional[RunContext]:
        if args:
            # recognize first argument as a command
            first = args.reset().peek_current()
            rule: SubcommandRule = self._find_rule(SubcommandRule, first)
            if rule:
                args.pop_current()
                subparser = Parser(rule.subrules, rule.run, parent=self, subcommand=rule)
                return subparser._parse_args_queue(args)
        return None

    def _parse_positional_arguments(self, args: ArgsQue):
        for arg, rule in zip(args.reset(), self._rules(PositionalArgumentRule)):
            try:
                self.internal_vars[rule.name] = parse_value_rule(rule, args.pop_current())
            except ValueError as e:
                raise CliSyntaxError(f'parsing positional argument "{rule.name}"') from e

        if self.__parent and not self.__action_triggered:
            self.__parent._parse_positional_arguments(args)

    def _parse_many_arguments(self, args: ArgsQue):
        args.reset()
        for rule in self._rules(ManyArgumentsRule):
            retrieve_count: Optional[int] = rule.count_max()
            if not retrieve_count:
                retrieve_count = len(args)
            if len(args) < retrieve_count:
                raise CliSyntaxError(f'{retrieve_count} positional arguments are required,'
                                     f' but "{len(args)} given"')
            retrieved = []
            for _ in range(retrieve_count):
                arg = args.pop_current()
                try:
                    parsed_value = parse_value_rule(rule, arg)
                    retrieved.append(parsed_value)
                except ValueError as e:
                    raise CliSyntaxError(f'parsing many arguments "{rule.name}"') from e

            if rule.joined_with:
                var_value = rule.joined_with.join(retrieved)
            else:
                var_value = retrieved
            self.internal_vars[rule.name] = var_value

        if self.__parent:
            self.__parent._parse_many_arguments(args)

    def _run_default_action(self) -> Optional[RunContext]:
        if self.__dry or self.__run:
            return self._build_run_context(self.__run)
        elif self.__parent:
            return self.__parent._run_default_action()
        return None

    def _check_superfluous_args(self, args: ArgsQue):
        if args and not self.__dry:
            if self.__error_unrecognized:
                raise CliSyntaxError(f'unrecognized arguments: {" ".join(args)}')
            else:
                log.warn(f'unrecognized arguments: {" ".join(args)}')

    def _check_required_arguments(self):
        check_required_arguments(self.__rules, self.internal_vars)
        if self.__parent and not self.__action_triggered:
            self.__parent._check_required_arguments()

    def _check_strict_choices(self):
        check_strict_choices(self._rules(ValueRule), self.internal_vars)
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
            return {**self.__parent._internal_vars_merged(), **self.internal_vars.vars}
        return self.internal_vars.vars

    def _build_run_context(self, action: Optional[Action]) -> RunContext:
        internal_vars = self._internal_vars_merged()
        args_container = ArgsContainer(internal_vars)
        active_subcommands = self._active_subcommands()
        active_rules = self._active_rules()
        return RunContext(args_container, action, active_subcommands, active_rules, internal_vars)

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
