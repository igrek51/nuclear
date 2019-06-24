from typing import List, Type

from cliglue.builder.rule import CliRule, KeywordRule, TCliRule
from cliglue.parser.keyword import keywords_from_names


def filter_rules(rules: List[CliRule], *types: Type[TCliRule]) -> List[TCliRule]:
    return [r for r in rules if isinstance(r, (*types,))]


def normalize_keywords(rules: List[KeywordRule]):
    for rule in rules:
        rule.keywords = keywords_from_names(set(rule.keywords))
