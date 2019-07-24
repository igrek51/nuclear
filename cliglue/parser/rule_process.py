from typing import List, Type, Any

from cliglue.builder.rule import CliRule, KeywordRule, TCliRule, ValueRule
from cliglue.builder.typedef import TypeOrParser
from .keyword import format_keywords


def filter_rules(rules: List[CliRule], *types: Type[TCliRule]) -> List[TCliRule]:
    return [r for r in rules if isinstance(r, (*types,))]


def normalize_keywords(rules: List[KeywordRule]):
    for rule in rules:
        rule.keywords = format_keywords(set(rule.keywords))


def parse_rule_value(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    # custom parser
    if callable(_type):
        return _type(arg)
    # cast to custom type or default types
    return _type(arg)
