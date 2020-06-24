from typing import List, Type

from nuclear.builder.rule import CliRule, KeywordRule, TCliRule
from .keyword import format_keywords


def filter_rules(rules: List[CliRule], *types: Type[TCliRule]) -> List[TCliRule]:
    return [r for r in rules if isinstance(r, (*types,))]


def normalize_keywords(rules: List[KeywordRule]):
    for rule in rules:
        rule.keywords = format_keywords(set(rule.keywords))
