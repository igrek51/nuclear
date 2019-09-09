from collections.abc import Iterable
from typing import List, Any

from cliglue.builder.rule import ValueRule
from cliglue.builder.typedef import TypeOrParser


def parse_value_rule(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    if _type is None:
        return arg
    # invoke custom parser or cast to custom type
    return _type(arg)


def generate_value_choices(rule: ValueRule) -> List[Any]:
    if not rule.choices:
        return []
    elif isinstance(rule.choices, list):
        return rule.choices
    elif isinstance(rule.choices, Iterable):
        return [choice for choice in rule.choices]
    else:
        return list(rule.choices())
