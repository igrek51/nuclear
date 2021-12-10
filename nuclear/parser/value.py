import inspect
from collections.abc import Iterable
from typing import List, Any, Optional

from nuclear.builder.rule import ValueRule
from nuclear.builder.typedef import TypeOrParser
from nuclear.types.boolean import boolean


def parse_value_rule(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    if _type is None:
        return arg
    if _type == bool:
        return boolean(arg)
    # invoke custom parser or cast to custom type
    return _type(arg)


def generate_value_choices(rule: ValueRule, current: Optional[str] = None) -> List[Any]:
    if not rule.choices:
        return []
    elif isinstance(rule.choices, list):
        return rule.choices
    elif isinstance(rule.choices, Iterable):
        return [choice for choice in rule.choices]
    else:
        (args, _, _, _, _, _, annotations) = inspect.getfullargspec(rule.choices)
        if len(args) >= 1:
            results = rule.choices(current=current)
        else:
            results = rule.choices()
        return list(results)
