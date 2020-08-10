import os
import sys
import traceback
from contextlib import contextmanager
from typing import Dict, Any, Collection

from .context_logger import log
from .wrap_error import ContextError


@contextmanager
def logerr(context_name: str = '', print_traceback: bool = True):
    """Catches all exceptions and displays traceback in pretty, concise format"""
    try:
        yield
    except KeyboardInterrupt:
        print()
        log.debug('KeyboardInterrupt')
        exit(1)
    except ContextError as e:
        _print_error_context(e, e.ctx, print_traceback, context_name)
    except Exception as e:
        _print_error_context(e, {}, print_traceback, context_name)


def _print_error_context(e: Exception, ctx: Dict[str, Any], print_traceback: bool, context_name: str):
    if print_traceback:
        ex_type, ex, tb = sys.exc_info()

        # got from traceback.format_exception(ex_type, ex, tb)
        t1 = traceback.TracebackException(type(ex_type), ex, tb, limit=None)
        while t1.__cause__ is not None:
            t1 = t1.__cause__

        frames: Collection[traceback.FrameSummary] = traceback.extract_tb(t1.exc_traceback)

        # hide traceback from this file
        lines = [f'{os.path.normpath(frame.filename)}:{frame.lineno}' for frame in frames
                 if _include_traceback_frame(frame)]

        tb = ','.join(lines)
        ctx['cause'] = _root_cause_type(e)
        ctx['traceback'] = tb
    error_msg = _error_message(e, context_name)
    log.error(error_msg, **ctx)


def _root_cause_type(e: Exception) -> str:
    while e.__cause__ is not None:
        e = e.__cause__
    return type(e).__name__


def _include_traceback_frame(frame: traceback.FrameSummary) -> bool:
    return not os.path.exists(frame.filename) or not os.path.samefile(frame.filename, __file__)


def _error_message(e: Exception, context_name: str):
    if not context_name:
        return str(e)
    return f'{context_name}: {e}'
