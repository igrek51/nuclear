from typing import Union, Callable, Iterable, List, Type, Any

Action = Callable[..., None]
ChoiceProvider = Union[Iterable[Any], Callable[..., List[Any]]]
TypeOrParser = Union[Type, Callable[[str], Any]]
