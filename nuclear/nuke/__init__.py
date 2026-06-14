import atexit
import os
import sys
from typing import TypeVar, Type, Optional

from .config import load_config, NukeConfig
from .shell import sh, ShellRunner
from .paths import validate_sources
from .invoke import run, depends

T = TypeVar('T')


def _discover_config() -> Type:
    main_module = sys.modules.get('__main__')
    if main_module is not None:
        candidate = getattr(main_module, 'Config', None)
        if candidate is not None and isinstance(candidate, type) and hasattr(candidate, '__annotations__'):
            return candidate
    return NukeConfig


def init(
    config_class: Optional[Type[T]] = None,
    print_log: bool = True,
    raw_output: bool = True,
    auto_run: bool = True,
    **sh_options,
) -> tuple[T, ShellRunner]:
    """Initialize config and shell runner in one call.
    
    Automatically passes the 'dry' flag from config to shell runner if present.
    
    Usage:
        # Auto-discover Config, auto-run at exit:
        config, sh = nuke.init()
        
        # With custom config:
        config, sh = nuke.init(Config, raw_output=True, print_log=True)
    
    Args:
        config_class: Configuration class to load from .config.yaml + CLI args.
                     Defaults to auto-discovered 'Config' class or 'NukeConfig'.
        auto_run: Whether to register nuke.run() as an atexit handler.
        **sh_options: Options to pass to sh() (raw_output, print_log, etc.)
    
    Returns:
        Tuple of (config instance, ShellRunner instance)
    """
    if config_class is None:
        config_class = _discover_config()
    config = load_config(config_class)
    sh_options.setdefault('dry', getattr(config, 'dry', False))
    
    if auto_run:
        main_module = sys.modules.get('__main__')
        # Register atexit only if running as a script directly, not during imports or tests
        if main_module is not None and getattr(main_module, '__spec__', None) is None and os.environ.get('NUKE_TESTING') != '1':
            atexit.register(run)
            
    return config, sh(print_log=print_log, raw_output=raw_output, **sh_options)
