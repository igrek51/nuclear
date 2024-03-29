import inspect
from collections.abc import Iterable
from typing import List, Any, Optional

from nuclear.cli.builder.rule import ValueRule
from nuclear.cli.builder.typedef import TypeOrParser
from nuclear.cli.parser.error import CliSyntaxError
from nuclear.cli.types.boolean import boolean


def parse_value_rule(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    if _type is None:
        return arg
    if _type == bool:
        return boolean(arg)
    _type_name = str(_type)
    if _type_name.startswith('typing.Union['):
        try:
            return _parse_union_value(_type, arg)
        except _TypeNotMatched:
            raise CliSyntaxError(f"variable '{arg}' didn't match Union type: {_type}")
    elif _type_name.startswith('typing.'):
        return arg
    # invoke custom parser or cast to custom type
    return _type(arg)


class _TypeNotMatched(RuntimeError):
    pass


def _parse_union_value(_type: TypeOrParser, arg: str) -> Any:
    try:
        utypes = _type.__args__
    except AttributeError:
        return arg
    for utype in utypes:
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
