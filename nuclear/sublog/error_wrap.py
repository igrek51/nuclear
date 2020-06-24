import os
import sys
import traceback
from contextlib import contextmanager

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
    try:
        yield
    except ContextError as e:
        if print_traceback:
            ex_type, ex, tb = sys.exc_info()

            # got from traceback.format_exception(ex_type, ex, tb)
            t1 = traceback.TracebackException(type(ex_type), ex, tb, limit=None)
            while t1.__cause__ is not None:
                t1 = t1.__cause__

            frames = traceback.extract_tb(t1.exc_traceback)

            # hide traceback from this file
            lines = [f'{frame.filename}:{frame.lineno}' for frame in frames
                     if not os.path.samefile(frame.filename, __file__)]

            tb = ','.join(lines)
            e.ctx['traceback'] = tb

        log.error(str(e), **e.ctx)
    except KeyboardInterrupt:
        print()
        log.debug('KeyboardInterrupt')
        exit(1)
    except Exception as e:
        log.error(str(e))
