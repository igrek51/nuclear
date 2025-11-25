import inspect
import re
import sys
from typing import Any

from nuclear.sublog import logger, error_handler
from nuclear.nuke.config import apply_overrides


def run():
    with error_handler():
        _run_with_args(sys.argv[1:])


def _run_with_args(args: list[str]):
    if not args:
        return _show_available_targets()

    positionals, overrides = parse_cli_args(args)
    _apply_cli_overrides_to_config(overrides)

    function_names: list[str] = _list_target_names()
    for arg in positionals:
        assert arg in function_names, f'unknown target function: {arg}'
    
    main_module = sys.modules['__main__']
    for arg in positionals:
        function = getattr(main_module, arg)
        logger.info(f'Calling function: {arg}')
        function()


def parse_cli_args(args: list[str]) -> tuple[list[str], dict[str, str]]:
    """
    Extract CLI parameters in the format:
        --name=value goes as {'name': 'value'} in the overrides dict
        --param-name is extracted as {'param_name': '1'} in the overrides dict - interpreted as flag
        --long-name="long value" is extracted as {'long_name': 'long value'}
    Once the parameter or flag is detected, it is dropped from the list.
    The rest that stays at the end, are the positional arguments.
    Return tuple of positional arguments and the dict of extracted parameters / flags.
    """
    positional_args: list[str] = []
    overrides: dict[str, str] = {}

    remaining_args = list(args)
    i = 0
    while i < len(remaining_args):
        arg = remaining_args[i]
        if arg.startswith('--'):
            match = re.fullmatch(r'--([a-zA-Z0-9_-]+)(?:=(.*))?', arg)
            if match:
                key = match.group(1).replace('-', '_')
                value = match.group(2)
                if value is None: # flag
                    overrides[key] = '1'
                else: # key-value pair
                    overrides[key] = value.strip('\'"') # remove surrounding quotes
                remaining_args.pop(i)
                continue
        positional_args.append(arg)
        i += 1
    return positional_args, overrides


def _apply_cli_overrides_to_config(overrides: dict[str, str]):
    main_module = sys.modules['__main__']
    if not hasattr(main_module, 'config'):
        if overrides:
            logger.warn("Can't find \"config\" object in the main module")
        return

    config = getattr(main_module, 'config')

    apply_cli_overrides(config, overrides)


def apply_cli_overrides(config: Any, overrides: dict[str, str]):
    Config = type(config)
    apply_overrides(config, Config, overrides)


def _show_available_targets():
    function_names: list[str] = _list_target_names()
    if not function_names:
        logger.warn('No available target functions - add public function in the main module')
        return
    
    logger.info('Available target functions', functions=len(function_names))
    for name in function_names:
        print(name)


def _list_target_names() -> list[str]:
    main_module = sys.modules['__main__']
    attrs: list[str] = dir(main_module)
    public_attrs = [a for a in attrs if not a.startswith('_')]
    return [a for a in public_attrs if inspect.isfunction(getattr(main_module, a))]
