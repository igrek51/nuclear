import os
import traceback
from typing import Collection, Iterable, Dict, Optional, Tuple

from nuclear.sublog.context_error import ContextError


def exception_details(e: BaseException) -> str:
    """
    Return concise one-line details of exception, containing message, exception type and short traceback
    """
    ex_type: type[BaseException] = type(e)
    tb = e.__traceback__

    traceback_ex = traceback.TracebackException(ex_type, e, tb, limit=None)
    traceback_lines = list(_get_traceback_lines(traceback_ex))
    traceback_str = ', '.join(traceback_lines)
    cause = _root_cause_type(e)
    error_msg = _error_message(e)
    return f'{error_msg}: cause={cause}, traceback={traceback_str}'


def extended_exception_details(e: BaseException) -> Tuple[str, Dict]:
    if isinstance(e, ContextError):
        ctx = e.ctx
    else:
        ctx = {}

    ex_type = type(e)
    traceback_ex = traceback.TracebackException(ex_type, e, e.__traceback__, limit=None)
    traceback_lines = list(_get_traceback_lines(traceback_ex))
    traceback_str = ', '.join(traceback_lines)
    ctx['cause'] = _root_cause_type(e)
    ctx['traceback'] = traceback_str
    error_msg = _error_message(e)
    return error_msg, ctx


def unwrap(e: BaseException) -> BaseException:
    """Find root cause of the error"""
    while e.__cause__ is not None:
        e = e.__cause__
    return e


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


def _root_cause_type(e: BaseException) -> str:
    while e.__cause__ is not None:
        e = e.__cause__
    return type(e).__name__


def _error_message(e: BaseException, context_name: str = ''):
    layers = []
    if context_name:
        layers.append(context_name)
    e_step: Optional[BaseException] = e
    while e_step is not None:
        if isinstance(e_step, ContextError):
            layers.append(e_step.context_message.strip())
        else:
            layers.append(str(e_step).strip())
        e_step = e_step.__cause__
    return ': '.join(layers)
