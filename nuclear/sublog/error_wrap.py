import os
import sys
import traceback
from contextlib import contextmanager
from typing import Dict, Any

from .context_logger import log


class ContextError(RuntimeError):
    def __init__(self, message: str, **ctx):
        super().__init__(message)
        self.ctx = ctx


@contextmanager
def wrap_context(context_name: str, **ctx):
    try:
        yield
    except ContextError as e:
        merged_context = {**ctx, **e.ctx}
        raise ContextError(f'{context_name}: {e}', **merged_context) from e
    except Exception as e:
        raise ContextError(f'{context_name}: {e}', **ctx) from e


@contextmanager
def log_error(print_traceback: bool = True):
    """Deprecated, use logerr instead"""
    try:
        yield
    except KeyboardInterrupt:
        print()
        log.debug('KeyboardInterrupt')
        exit(1)
    except ContextError as e:
        _print_error_context(str(e), e.ctx, print_traceback)
    except Exception as e:
        _print_error_context(str(e), {}, print_traceback)


@contextmanager
def logerr(print_traceback: bool = True):
    """Catches all exceptions and displays traceback in pretty, concise format"""
    try:
        yield
    except KeyboardInterrupt:
        print()
        log.debug('KeyboardInterrupt')
        exit(1)
    except ContextError as e:
        _print_error_context(str(e), e.ctx, print_traceback)
    except Exception as e:
        _print_error_context(str(e), {}, print_traceback)


def _print_error_context(message: str, ctx: Dict[str, Any], print_traceback: bool):
    if print_traceback:
        ex_type, ex, tb = sys.exc_info()

        # got from traceback.format_exception(ex_type, ex, tb)
        t1 = traceback.TracebackException(type(ex_type), ex, tb, limit=None)
        while t1.__cause__ is not None:
            t1 = t1.__cause__

        frames = traceback.extract_tb(t1.exc_traceback)

        # hide traceback from this file
        lines = [f'{os.path.normpath(frame.filename)}:{frame.lineno}' for frame in frames
                 if not os.path.samefile(frame.filename, __file__)]

        tb = ','.join(lines)
        ctx['traceback'] = tb
    log.error(message, **ctx)
