import inspect
import sys

from nuclear.sublog import logger, error_handler


def run():
    with error_handler():
        _run_with_args(sys.argv[1:])


def _run_with_args(args: list[str]):
    if not args:
        return _list_targets()

    function_names: list[str] = _list_target_names()
    for arg in args:
        assert arg in function_names, f'unknown target function: {arg}'
    
    main_module = sys.modules['__main__']
    for arg in args:
        function = getattr(main_module, arg)
        logger.info(f'Calling function: {arg}')
        function()


def _list_targets():
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
