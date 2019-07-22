from typing import List

from cliglue.builder.rule import CliRule, PositionalArgumentRule, ManyArgumentsRule, \
    OptionalValueRule
from cliglue.parser.error import CliDefinitionError
from cliglue.parser.rule_process import filter_rules


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
