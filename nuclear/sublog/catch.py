import os
import traceback
from contextlib import contextmanager
from typing import Dict, Any, Collection, Iterable

from .context_logger import log
from .wrap_error import ContextError


@contextmanager
def logerr(context_name: str = '', print_traceback: bool = True):
    """
    Catch all exceptions and display traceback in pretty, concise format
    :param context_name: description of the operation to show in case of error
    :param print_traceback: whether to print traceback or not in case of error
    """
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
        ex_type = type(e)
        tb = e.__traceback__
        traceback_ex = traceback.TracebackException(ex_type, e, tb, limit=None)
        traceback_lines = list(_get_traceback_lines(traceback_ex))
        traceback_str = ', '.join(traceback_lines)
        ctx['cause'] = _root_cause_type(e)
        ctx['traceback'] = traceback_str
    error_msg = _error_message(e, context_name)
    log.error(error_msg, **ctx)


def log_exception(e: BaseException, print_traceback: bool = True):
    """
    Log exception in concise one-line format containing message, exception type and short traceback
    """
    _print_error_context(e, {}, print_traceback, '')


def short_exception_details(e: BaseException) -> str:
    """
    Return concise one-line details of exception, containing message, exception type and short traceback
    """
    return _get_exc_info_details(type(e), e, e.__traceback__)


def _get_exc_info_details(ex_type, e, tb) -> str:
    traceback_ex = traceback.TracebackException(ex_type, e, tb, limit=None)
    traceback_lines = list(_get_traceback_lines(traceback_ex))
    traceback_str = ', '.join(traceback_lines)
    cause = _root_cause_type(e)
    error_msg = _error_message(e).strip()
    return f'{error_msg}, cause={cause}, traceback={traceback_str}'


def _root_cause_type(e: Exception) -> str:
    while e.__cause__ is not None:
        e = e.__cause__
    return type(e).__name__


def _get_traceback_lines(t1: traceback.TracebackException) -> Iterable[str]:
    # get last cause only
    while t1.__cause__ is not None:
        t1 = t1.__cause__

    frames: Collection[traceback.FrameSummary] = t1.stack
    for frame in frames:
        if _include_traceback_frame(frame):  # hide traceback from this file
            yield f'{os.path.normpath(frame.filename)}:{frame.lineno}'


def _include_traceback_frame(frame: traceback.FrameSummary) -> bool:
    if not os.path.exists(frame.filename):
        return True

    frame_dir = os.path.dirname(frame.filename)
    if not os.path.exists(frame_dir):
        return True

    nuclear_dir = os.path.dirname(__file__)
    if not os.path.exists(nuclear_dir):
        return True

    if os.path.samefile(frame_dir, nuclear_dir):
        return False
    return True


def _error_message(e: Exception, context_name: str = ''):
    layers = []
    if context_name:
        layers.append(context_name)
    while e is not None:
        if isinstance(e, ContextError):
            layers.append(e.context_message)
        else:
            layers.append(str(e))
        e = e.__cause__
    return ': '.join(layers)
