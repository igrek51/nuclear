from typing import Union, Callable, Iterable, List, Type, Any, Optional

Action = Callable[..., None]
ChoiceProvider = Union[Iterable[Any], Callable[[Optional[str]], List[Any]]]
TypeOrParser = Union[Type, Callable[[str], Any]]
