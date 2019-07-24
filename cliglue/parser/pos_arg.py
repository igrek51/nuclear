from typing import Optional

from cliglue.builder.rule import ManyArgumentsRule


def many_arguments_min_count(rule: ManyArgumentsRule) -> Optional[int]:
    if rule.count:
        return rule.count
    return rule.min_count


def many_arguments_max_count(rule: ManyArgumentsRule) -> Optional[int]:
    if rule.count:
        return rule.count
    return rule.max_count
