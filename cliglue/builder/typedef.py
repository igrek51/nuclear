from typing import Union, Callable, List, Type, Any

Action = Callable[..., None]
ChoiceProvider = Union[List[Any], Callable[..., List[Any]]]
TypeOrParser = Union[Type, Callable[[str], Any]]
