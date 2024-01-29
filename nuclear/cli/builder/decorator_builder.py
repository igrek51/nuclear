from typing import Callable, List, Optional, Tuple, Dict, Any
from inspect import getfullargspec, getdoc
import re

from .rule import SubcommandRule
from .rule_factory import argument, arguments, flag, parameter, subcommand


def create_decorated_subcommand(function: Callable[..., None], keyword: str) -> SubcommandRule:
    docstring = getdoc(function)
    function_help, params_help = _parse_function_help(docstring)
    rule = subcommand(keyword, run=function, help=function_help)
    _add_subcommand_arguments(rule, function, params_help)
    return rule


def _parse_function_help(docstring: Optional[str]) -> Tuple[Optional[str], Dict[str, str]]:
    if not docstring:
        return None, {}
    
    function_help_lines = []
    params_help = {}
    params_reached = False
    param_regex = re.compile(":param (.+): (.+)")
    for line in docstring.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(':'):
            params_reached = True
        if not params_reached:
            function_help_lines.append(line)
        param_match = param_regex.fullmatch(line)
        if param_match:
            param_name = param_match.group(1)
            param_help = param_match.group(2)
            params_help[param_name] = param_help

    return '\n'.join(function_help_lines), params_help


def _add_subcommand_arguments(
    subcommand_rule: SubcommandRule,
    function: Callable[..., None],
    params_help: Dict[str, str],
):
    args, varargs, _, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(function)
    required_args_len = len(args) - len(defaults) if defaults is not None else len(args)
    required_args = args[:required_args_len]
    optional_args = args[required_args_len:]
    _add_subcommand_required_arguments(subcommand_rule, required_args, varargs, annotations, params_help)
    _add_subcommand_optional_parameters(subcommand_rule, optional_args, defaults, kwonlyargs, kwonlydefaults,
                                        annotations, params_help)


def _add_subcommand_required_arguments(
    subcommand_rule: SubcommandRule,
    required_args: List[str],
    varargs: Optional[str],
    annotations: Dict,
    params_help: Dict[str, str],
):
    for arg in required_args:
        typo = annotations.get(arg, str)
        help = params_help.get(arg)
        subcommand_rule.has(argument(arg, type=typo, help=help))
    
    if varargs is not None:
        typo = annotations.get(varargs, str)
        help = params_help.get(varargs)
        subcommand_rule.has(arguments(varargs, type=typo, help=help))


def _add_subcommand_optional_parameters(
    subcommand_rule: SubcommandRule,
    optional_args: List[str],
    defaults: Optional[Tuple],
    kwonlyargs: List[str],
    kwonlydefaults: Optional[Dict[str, Any]],
    annotations: Dict[str, str],
    params_help: Dict[str, str],
):
    for i, arg in enumerate(optional_args):
        typo = annotations.get(arg, str)
        default_value = defaults[i] if defaults is not None else None
        help = params_help.get(arg)
        if typo == bool and default_value is False:
            subcommand_rule.has(flag(arg, help=help))
        else:
            subcommand_rule.has(parameter(arg, type=typo, default=default_value, help=help))

    if not kwonlydefaults:
        kwonlydefaults = dict()
    for arg in kwonlyargs:
        typo = annotations.get(arg, str)
        default_value = kwonlydefaults.get(arg)
        help = params_help.get(arg)
        if typo == bool and (default_value is None or default_value is False):
            subcommand_rule.has(flag(arg, help=help))
        else:
            subcommand_rule.has(parameter(arg, type=typo, default=default_value, help=help))
