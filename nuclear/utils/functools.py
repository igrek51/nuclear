from inspect import getfullargspec
from typing import Callable, Dict, Any


def safe_call(function: Callable, **kwargs):
    """
    Call a function, omitting redundant arguments that are absent in the real function signature.
    """
    args, varargs, _, _, kwonlyargs, _, _ = getfullargspec(function)
    expected_arguments: set[str] = set()  # arguments declared in the function implementation
    for arg in args:
        expected_arguments.add(arg)
    if varargs is not None:
        expected_arguments.add(varargs)
    for arg in kwonlyargs:
        expected_arguments.add(arg)

    adjusted_kwargs: Dict[str, Any] = kwargs.copy()
    for key in kwargs.keys():
        if key not in expected_arguments:
            del adjusted_kwargs[key]

    return function(**adjusted_kwargs)
