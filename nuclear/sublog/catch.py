from contextlib import contextmanager
import traceback
from typing import Dict, Any

from nuclear.sublog.exception import _error_message, _get_traceback_lines, _root_cause_type
from nuclear.sublog.logging import logger
from nuclear.sublog.context_error import ContextError


@contextmanager
def error_handler(context_name: str = ''):
    """
    Catch all exceptions and display traceback in pretty, concise format
    :param context_name: description of the operation to show in case of error
    """
    try:
        yield
    except KeyboardInterrupt:
        print()
        logger.debug('KeyboardInterrupt')
        exit(1)
    except ContextError as e:
        _print_error_context(e, e.ctx, context_name)
    except Exception as e:
        _print_error_context(e, {}, context_name)


def _print_error_context(e: Exception, ctx: Dict[str, Any], context_name: str):
    ex_type = type(e)
    tb = e.__traceback__
    traceback_ex = traceback.TracebackException(ex_type, e, tb, limit=None)
    traceback_lines = list(_get_traceback_lines(traceback_ex))
    traceback_str = ', '.join(traceback_lines)
    ctx['cause'] = _root_cause_type(e)
    ctx['traceback'] = traceback_str
    error_msg = _error_message(e, context_name)
    logger.error(error_msg, **ctx)
