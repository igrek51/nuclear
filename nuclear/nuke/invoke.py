import inspect
import sys
from typing import Any

from nuclear.sublog import logger, error_handler


def run():
    with error_handler():
        _run_with_args(sys.argv[1:])


def _run_with_args(args: list[str]):
    if not args:
        return _show_available_targets()

    positional, overrides = parse_cli_args(args)

    config = _get_config_object()

    function_names: list[str] = _list_target_names()
    for arg in args:
        assert arg in function_names, f'unknown target function: {arg}'
    
    main_module = sys.modules['__main__']
    for arg in args:
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
    return [], {}


def _get_config_object() -> Any:
    main_module = sys.modules['__main__']
    if not hasattr(main_module, 'config'):
        logger.warn("Can't find config object in the main module")
        return {}
    return getattr(main_module, 'config')


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
