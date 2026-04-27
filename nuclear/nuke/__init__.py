from typing import TypeVar, Type, Optional

from .config import load_config, NukeConfig
from .shell import sh, ShellRunner
from .paths import validate_sources
from .invoke import run, depends

T = TypeVar('T')


def init(
    config_class: Optional[Type[T]] = None,
    print_log: bool = False,
    raw_output: bool = False,
    **sh_options,
) -> tuple[T, ShellRunner]:
    """Initialize config and shell runner in one call.
    
    Automatically passes the 'dry' flag from config to shell runner if present.
    
    Usage:
        # With default NukeConfig (only dry: bool = False)
        config, sh = nuke.init()
        
        # With custom config extending NukeConfig
        class Config(NukeConfig):
            limit: int = 0
        config, sh = nuke.init(Config, raw_output=True, print_log=True)
    
    Args:
        config_class: Configuration class to load from .config.yaml + CLI args.
                     Defaults to NukeConfig if not provided.
        **sh_options: Options to pass to sh() (raw_output, print_log, etc.)
    
    Returns:
        Tuple of (config instance, ShellRunner instance)
    """
    if config_class is None:
        config_class = NukeConfig
    config = load_config(config_class)
    sh_options.setdefault('dry', getattr(config, 'dry', False))
    return config, sh(print_log=print_log, raw_output=raw_output, **sh_options)
