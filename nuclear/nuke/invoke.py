import inspect
import re
import sys
from typing import Any, Optional, Type

from nuclear.sublog import logger, error_handler


# Track executed targets to avoid running them multiple times
_executed_targets: set[str] = set()


def depends(*target_names: str):
    """
    Decorator to mark target dependencies.

    Usage:
        @depends('build')
        def test():
            ...
    """
    def decorator(func):
        func.__depends__ = target_names
        return func
    return decorator


def run():
    with error_handler():
        _run_with_args(sys.argv[1:])


def _run_with_args(args: list[str]):
    _executed_targets.clear()

    if not args:
        return _show_available_targets()

    main_module = sys.modules['__main__']
    if '-h' in args or '--help' in args:
        config_class = getattr(main_module, 'Config', None)
        if config_class is not None and hasattr(config_class, '__annotations__'):
            return _show_help(config_class)
        return _show_help()

    config_class = getattr(main_module, 'Config', None)
    positionals, _ = parse_cli_args(args, config_class=config_class)
    positionals = [arg.replace('-', '_') for arg in positionals]

    function_names: list[str] = _list_target_names()
    for arg in positionals:
        assert arg in function_names, f'unknown target function: {arg}'

    for arg in positionals:
        _execute_target(main_module, arg)


def _execute_target(main_module, target_name: str):
    """Execute a target and its dependencies, ensuring each runs only once."""
    if target_name in _executed_targets:
        return

    function = getattr(main_module, target_name)

    # Execute dependencies first
    if hasattr(function, '__depends__'):
        for dep in function.__depends__:
            dep_normalized = dep.replace('-', '_')
            _execute_target(main_module, dep_normalized)

    logger.info(f'Calling function: {target_name}')
    function()
    _executed_targets.add(target_name)


def _is_nested_config_type(field_type: Type[Any]) -> bool:
    return (
        isinstance(field_type, type)
        and hasattr(field_type, '__annotations__')
        and bool(field_type.__annotations__)
    )


def _collect_bool_flags(clazz: Type[Any], prefix: str, result: set[str]):
    field_types = getattr(clazz, '__annotations__', {})
    for field_name, field_type in field_types.items():
        if field_type is bool:
            default_value = getattr(clazz, field_name, None)
            if default_value is False:
                result.add(f'{prefix}{field_name}')
        elif _is_nested_config_type(field_type):
            default_value = getattr(clazz, field_name, None)
            if default_value is not None:
                _collect_bool_flags(field_type, f'{prefix}{field_name}.', result)


def parse_cli_args(args: list[str], config_class: Optional[Type[Any]] = None) -> tuple[list[str], dict[str, str]]:
    """
    Extract CLI parameters in CLI format:
        --name=value goes as {'name': 'value'} in the overrides dict
        --name value goes as {'name': 'value'} in the overrides dict (when config_class is provided)
        --flag (standalone) is extracted as {'flag': '1'} - treated as boolean flag
        --long-name="long value" is extracted as {'long_name': 'long value'}
    
    Parameters may appear anywhere in the CLI arguments list (before or after positional args).
    
    A value is consumed after a flag if:
    - The flag uses --name=value format (explicit), OR
    - config_class is provided AND the next arg doesn't start with -- AND the flag is NOT a known boolean with default False
    
    If config_class is provided, it's used to determine which flags are boolean (and thus don't need values).
    If config_class is not provided, only --name=value format consumes values; standalone flags don't.
    
    The rest that stays at the end, are the positional arguments.
    Return tuple of positional arguments and the dict of extracted parameters / flags.
    """
    positional_args: list[str] = []
    overrides: dict[str, str] = {}
    
    # flags - boolean fields with default False (recursive for nested config types)
    bool_flags: set[str] = set()
    has_config = config_class is not None
    if has_config:
        _collect_bool_flags(config_class, '', bool_flags)

    remaining_args = list(args)
    i = 0
    while i < len(remaining_args):
        arg = remaining_args[i]
        if arg in {'--help', '-h'}:
           remaining_args.pop(i)
           continue
        if arg.startswith('--'):
            match = re.fullmatch(r'--([a-zA-Z0-9_.-]+)(?:=(.*))?', arg)
            if match:
                key = match.group(1).replace('-', '_')
                value = match.group(2)
                if value is not None:  # --name=value format (explicit)
                    overrides[key] = value.strip('\'"')  # remove surrounding quotes
                    remaining_args.pop(i)
                    continue
                elif has_config and i + 1 < len(remaining_args) and not remaining_args[i + 1].startswith('--'):
                    if key not in bool_flags:
                        next_arg = remaining_args[i + 1]
                        overrides[key] = next_arg.strip('\'"')
                        remaining_args.pop(i)
                        remaining_args.pop(i)  # pop again because first pop shifts indices
                        continue
                
                # Standalone flag (no value consumed)
                overrides[key] = '1'
                remaining_args.pop(i)
                continue
        positional_args.append(arg)
        i += 1
    return positional_args, overrides


def _show_available_targets():
    """List available target functions."""
    function_names: list[str] = _list_target_names()
    
    if not function_names:
        logger.warn('No available target functions - add public function in the main module')
        return
    
    main_module = sys.modules['__main__']
    
    print('Available target functions:')
    for name in function_names:
        func = getattr(main_module, name)
        docstring = inspect.getdoc(func)
        if docstring:
            first_line = docstring.split('\n')[0]
            print(f'  {name:<20} - {first_line}')
        else:
            print(f'  {name}')


def _print_config_params(clazz: Type[Any], prefix: str):
    annotations = getattr(clazz, '__annotations__', {})
    for param_name, param_type in annotations.items():
        if param_name.startswith('_'):
            continue
        default_value = getattr(clazz, param_name, None)
        full_name = f'{prefix}{param_name.replace("_", "-")}'
        if _is_nested_config_type(param_type):
            inner = getattr(clazz, param_name, None)
            if inner is not None:
                _print_config_params(param_type, f'{full_name}.')
        else:
            type_name = param_type.__name__ if hasattr(param_type, '__name__') else str(param_type)
            is_bool_flag = param_type is bool and default_value is False
            if is_bool_flag:
                print(f'  --{full_name:<24} Boolean flag (default: {default_value})')
            else:
                print(f'  --{full_name:<24} {type_name} (default: {default_value})')


def _show_help(config_class: Optional[Type[Any]] = None):
    """Show global help."""
    main_module = sys.modules['__main__']

    print('\nUsage: ./nukefile.py [OPTIONS] [TARGET]...')
    print('       ./nukefile.py --help')

    function_names: list[str] = _list_target_names()
    if function_names:
        print('\nAvailable target functions:')
        for name in function_names:
            func = getattr(main_module, name)
            docstring = inspect.getdoc(func)
            if docstring:
                first_line = docstring.split('\n')[0]
                print(f'  {name:<20} - {first_line}')
            else:
                print(f'  {name}')

    if config_class:
        print('\nConfiguration parameters (can be set via CLI or .config.yaml):\n')
        _print_config_params(config_class, '')

    print()


def _list_target_names() -> list[str]:
    main_module = sys.modules['__main__']
    attrs: list[str] = dir(main_module)
    public_attrs = [a for a in attrs if not a.startswith('_')]

    # Filter to include only functions defined in this module, not imported ones
    target_functions = []
    for attr_name in public_attrs:
        attr = getattr(main_module, attr_name)
        if inspect.isfunction(attr):
            # Check if the function is defined in the main module, not imported
            if attr.__module__ == main_module.__name__:
                target_functions.append(attr_name)

    return target_functions
