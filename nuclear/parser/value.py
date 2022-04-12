import inspect
from collections.abc import Iterable
from typing import List, Any, Optional, Union, get_origin, get_args

from nuclear.builder.rule import ValueRule
from nuclear.builder.typedef import TypeOrParser
from nuclear.parser.error import CliSyntaxError
from nuclear.types.boolean import boolean


def parse_value_rule(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    if _type is None:
        return arg
    if _type == bool:
        return boolean(arg)
    typing_origin = get_origin(_type)
    if typing_origin is Union:
        try:
            return _parse_union_value(_type, arg)
        except _TypeNotMatched:
            raise CliSyntaxError(f"variable '{arg}' didn't match Union type: {_type}")
    elif typing_origin is not None:
        return arg
    # invoke custom parser or cast to custom type
    return _type(arg)


class _TypeNotMatched(RuntimeError):
    pass


def _parse_union_value(_type: TypeOrParser, arg: str) -> Any:
    for utype in get_args(_type):
        if get_origin(utype) is Union:
            try:
                return _parse_union_value(utype, arg)
            except _TypeNotMatched:
                pass
        if utype == type(None) and arg is None:
            return None
        try:
            return utype(arg)
        except BaseException:
            pass
    raise _TypeNotMatched()


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
