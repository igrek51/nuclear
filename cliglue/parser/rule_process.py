from typing import List, Type, Optional

from cliglue.builder.rule import CliRule, KeywordRule, TCliRule, ManyArgumentsRule
from .keyword import keywords_from_names


def filter_rules(rules: List[CliRule], *types: Type[TCliRule]) -> List[TCliRule]:
    return [r for r in rules if isinstance(r, (*types,))]


def normalize_keywords(rules: List[KeywordRule]):
    for rule in rules:
        rule.keywords = keywords_from_names(set(rule.keywords))


def many_arguments_retrieve_count(rule: ManyArgumentsRule) -> Optional[int]:
    if rule.count:
        return rule.count
    return rule.max_count
