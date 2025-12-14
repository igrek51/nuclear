import sys
from pathlib import Path
import importlib.util

from nuclear.sublog import error_handler
from .invoke import _run_with_args


def main():
    """Entry point for the 'nuke' command-line tool."""
    with error_handler():
        nukefile_path = Path.cwd() / 'nukefile.py'

        if not nukefile_path.exists():
            raise FileNotFoundError(f'nukefile.py not found in {Path.cwd()}')

        # Load nukefile.py as a regular module (not as __main__)
        spec = importlib.util.spec_from_file_location('nukefile', nukefile_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f'Failed to load {nukefile_path}')

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Temporarily set as __main__ for invoke functions to find targets
        original_main = sys.modules.get('__main__')
        sys.modules['__main__'] = module
        try:
            _run_with_args(sys.argv[1:])
        finally:
            # Restore original __main__
            if original_main is not None:
                sys.modules['__main__'] = original_main


if __name__ == '__main__':
    main()
