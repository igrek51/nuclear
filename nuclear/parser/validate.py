from typing import List, Optional

from nuclear.builder.rule import CliRule, PositionalArgumentRule, ManyArgumentsRule, \
    OptionalValueRule, ValueRule, ParameterRule
from nuclear.parser.internal_vars import InternalVars
from .error import CliDefinitionError, CliSyntaxError
from .transform import filter_rules
from .value import generate_value_choices


def validate_rules(all_rules: List[CliRule]):
    for rule in filter_rules(all_rules, OptionalValueRule):
        if rule.required and rule.default:
            raise CliDefinitionError('argument value may be either required or have the default value')

    unlimited_args = 0
    for rule in filter_rules(all_rules, PositionalArgumentRule, ManyArgumentsRule):
        if isinstance(rule, PositionalArgumentRule):
            if unlimited_args:
                raise CliDefinitionError('positional argument can\'t be placed after unlimited many arguments rule')
        elif isinstance(rule, ManyArgumentsRule):
            if not rule.max_count and not rule.count:
                unlimited_args += 1


def check_required_arguments(rules: List[CliRule], internal_vars: InternalVars):
    for rule in filter_rules(rules, ParameterRule):
        if rule.required:
            for name in rule.var_names():
                if internal_vars[name] is None:
                    raise CliSyntaxError(f'required parameter "{", ".join(rule.keywords)}" is not given')

    for rule in filter_rules(rules, PositionalArgumentRule):
        if rule.required:
            if internal_vars[rule.name] is None:
                raise CliSyntaxError(f'required positional argument "{rule.name}" is not given')

    for rule in filter_rules(rules, ManyArgumentsRule):
        expected_count: Optional[int] = rule.count_min()
        if expected_count:
            given_count = len(internal_vars[rule.name])
            if given_count != expected_count:
                raise CliSyntaxError(f'"{expected_count}" arguments are required, but "{given_count}" were given')


def check_strict_choices(rules: List[ValueRule], internal_vars: InternalVars):
    for rule in rules:
        if rule.strict_choices and rule.choices:
            available_choices = generate_value_choices(rule)

            if isinstance(rule, ParameterRule):
                for name in rule.var_names():
                    if rule.multiple:
                        for var_value in internal_vars[name]:
                            if var_value not in available_choices:
                                raise CliSyntaxError(
                                    f'parameter value {var_value} does not belong to available choices: '
                                    f'{available_choices}')
                    else:
                        var_value = internal_vars[name]
                        if var_value not in available_choices:
                            raise CliSyntaxError(f'parameter value {var_value} does not belong to available choices: '
                                                 f'{available_choices}')

            elif isinstance(rule, PositionalArgumentRule):
                var_value = internal_vars[rule.name]
                if var_value not in available_choices:
                    raise CliSyntaxError(
                        f'positional argument value {var_value} does not belong to available choices: '
                        f'{available_choices}')

            elif isinstance(rule, ManyArgumentsRule):
                var_values: List = internal_vars[rule.name]
                for var_value in var_values:
                    if var_value not in available_choices:
                        raise CliSyntaxError(
                            f'one of arguments value {var_value} does not belong to available choices: '
                            f'{available_choices}')
