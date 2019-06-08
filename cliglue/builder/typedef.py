from typing import Union, Callable, List, Type, Any

Action = Callable[..., None]
ChoiceProvider = Union[List[str], Callable[..., List[str]]]
TypeOrParser = Union[Type, Callable[[str], Any]]
