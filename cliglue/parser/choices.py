import inspect
from typing import List, Any

from cliglue.builder.rule import ValueRule


def generate_value_choices(rule: ValueRule) -> List[Any]:
    if not rule.choices:
        return []
    elif isinstance(rule.choices, list):
        return rule.choices
    else:
        (args, _, _, _, _, _, _) = inspect.getfullargspec(rule.choices)
        return rule.choices()
