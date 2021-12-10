from typing import List, Any, Set, Optional, TypeVar, Iterable, Union

from dataclasses import dataclass, field

from nuclear.parser.keyword import format_var_names
from .typedef import Action, ChoiceProvider, TypeOrParser


@dataclass
class CliRule:
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


@dataclass
class ValueRule(CliRule):
    name: Optional[str] = None
    type: TypeOrParser = str
    choices: ChoiceProvider = None
    strict_choices: bool = False


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

    def default_value(self) -> Union[bool, int]:
        if self.multiple:
            return 0
        else:
            return False


@dataclass
class DictionaryRule(HelpRule, KeywordRule):
    name: Optional[str] = None
    key_type: TypeOrParser = str
    value_type: TypeOrParser = str

    def var_names(self) -> Iterable[str]:
        if self.name:
            return [self.name]
        else:
            return format_var_names(self.keywords)


@dataclass
class ParameterRule(HelpRule, OptionalValueRule, KeywordRule):
    multiple: bool = False

    def display_name(self) -> str:
        if self.name:
            return self.name
        else:
            return ', '.join(self.keywords)

    def var_names(self) -> Iterable[str]:
        if self.name:
            return [self.name]
        else:
            return format_var_names(self.keywords)

    def default_value(self) -> Any:
        if self.multiple:
            if not self.default:
                return []
            elif not isinstance(self.default, list):
                return [self.default]
            else:
                return self.default
        else:
            return self.default


@dataclass
class PositionalArgumentRule(HelpRule, OptionalValueRule):
    pass


@dataclass
class ManyArgumentsRule(HelpRule, ValueRule):
    count: Optional[int] = None
    min_count: Optional[int] = None
    max_count: Optional[int] = None
    joined_with: Optional[str] = None

    def count_min(self) -> Optional[int]:
        if self.count:
            return self.count
        return self.min_count

    def count_max(self) -> Optional[int]:
        if self.count:
            return self.count
        return self.max_count


@dataclass
class DefaultActionRule(CliRule):
    run: Action = None


TCliRule = TypeVar('TCliRule', bound=CliRule)
