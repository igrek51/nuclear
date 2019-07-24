from typing import Union

from cliglue.builder.rule import FlagRule


def flag_default_value(rule: FlagRule) -> Union[bool, int]:
    if rule.multiple:
        return 0
    else:
        return False
