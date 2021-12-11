from typing import Callable, List, Optional, Tuple, Dict, Any
from inspect import getfullargspec, getdoc

from .rule import SubcommandRule
from .rule_factory import argument, arguments, flag, parameter, subcommand


def create_decorated_subcommand(function: Callable[..., None], keyword: str) -> SubcommandRule:
    help = getdoc(function)
    if help:
        help = help.strip()
    rule = subcommand(keyword, run=function, help=help)
    _add_subcommand_arguments(rule, function)
    return rule


def _add_subcommand_arguments(subcommand: SubcommandRule, function: Callable[..., None]):
    args, varargs, _, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(function)
    required_args_len = len(args) - len(defaults) if defaults is not None else len(args)
    required_args = args[:required_args_len]
    optional_args = args[required_args_len:]
    _add_subcommand_required_arguments(subcommand, required_args, varargs, annotations)
    _add_subcommand_optional_parameters(subcommand, optional_args, defaults, kwonlyargs, kwonlydefaults, annotations)


def _add_subcommand_required_arguments(
    subcommand: SubcommandRule,
    required_args: List[str],
    varargs: Optional[str],
    annotations: Dict,
):
    for arg in required_args:
        typo = annotations.get(arg, str)
        subcommand.has(argument(arg, type=typo))
    
    if varargs is not None:
        typo = annotations.get(varargs, str)
        subcommand.has(arguments(varargs, type=typo))


def _add_subcommand_optional_parameters(
    subcommand: SubcommandRule,
    optional_args: List[str],
    defaults: Optional[Tuple],
    kwonlyargs: List[str],
    kwonlydefaults: Optional[Dict[str, Any]],
    annotations: Dict[str, str],
):
    for i, arg in enumerate(optional_args):
        typo = annotations.get(arg, str)
        default_value = defaults[i] if defaults is not None else None
        if typo == bool and default_value == False:
            subcommand.has(flag(arg))
        else:
            subcommand.has(parameter(arg, type=typo, default=default_value))

    if not kwonlydefaults:
        kwonlydefaults = dict()
    for arg in kwonlyargs:
        typo = annotations.get(arg, str)
        default_value = kwonlydefaults.get(arg)
        if typo == bool and (default_value is None or default_value == False):
            subcommand.has(flag(arg))
        else:
            subcommand.has(parameter(arg, type=typo, default=default_value))
