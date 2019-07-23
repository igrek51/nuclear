from typing import List, Any, Set, Optional, TypeVar

from dataclasses import dataclass, field

from .typedef import Action, ChoiceProvider, TypeOrParser


@dataclass
class CliRule(object):
    pass


@dataclass
class HelpRule(CliRule):
    help: str = None


@dataclass
class KeywordRule(CliRule):
    keywords: Set[str] = field(default_factory=lambda: set())


@dataclass
class ParentRule(KeywordRule):
    run: Action = None
    subrules: List['CliRule'] = field(default_factory=lambda: [])

    def has(self, *subrules: CliRule) -> 'ParentRule':
        self.subrules += subrules
        return self


# TODO validate value is in choices if given
@dataclass
class ValueRule(CliRule):
    name: Optional[str] = None
    type: TypeOrParser = Any
    choices: ChoiceProvider = None


@dataclass
class OptionalValueRule(ValueRule):
    required: bool = False
    default: Any = None


@dataclass
class SubcommandRule(ParentRule, HelpRule):
    pass


@dataclass
class PrimaryOptionRule(ParentRule, HelpRule):
    pass


@dataclass
class FlagRule(HelpRule, KeywordRule):
    multiple: bool = False


# TODO Dict value

@dataclass
class ParameterRule(HelpRule, OptionalValueRule, KeywordRule):
    multiple: bool = False


@dataclass
class PositionalArgumentRule(HelpRule, OptionalValueRule):
    pass


@dataclass
class ManyArgumentsRule(HelpRule, ValueRule):
    count: Optional[int] = None
    min_count: Optional[int] = None
    max_count: Optional[int] = None
    joined_with: Optional[str] = None


@dataclass
class DefaultActionRule(CliRule):
    run: Action = None


TCliRule = TypeVar('TCliRule', bound=CliRule)
