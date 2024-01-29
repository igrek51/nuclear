from contextlib import contextmanager
import logging
import os
import sys
import threading
from typing import Dict, Any

from colorama import Fore, Style

from nuclear.sublog.context_error import ContextError
from nuclear.sublog.exception import extended_exception_details

LOG_FORMAT = f'{Style.DIM}[%(asctime)s]{Style.RESET_ALL} %(levelname)s %(message)s'
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
LOGGING_LOGGER_NAME = 'nuclear.sublog'

log_level = os.environ.get('LOG_LEVEL', 'debug')
simultaneous_print_lock = threading.Lock()
_logging_logger = logging.getLogger(LOGGING_LOGGER_NAME)


def init_logs():
    """Configure loggers: formatters, handlers and log levels"""
    logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT, level=logging.INFO, datefmt=LOG_DATE_FORMAT, force=True)

    for handler in logging.getLogger().handlers:
        handler.setFormatter(ColoredFormatter(handler.formatter))

    level = _get_logging_level(log_level)
    root_logger = logging.getLogger(LOGGING_LOGGER_NAME)
    root_logger.setLevel(level)


def get_logger(logger_name: str) -> logging.Logger:
    """
    Get configured child logger
    :param logger_name: Name of the child logger. It's best to keep it __name__
    """
    logger = logging.getLogger(LOGGING_LOGGER_NAME)
    return logger.getChild(logger_name)


class ContextLogger:
    def __init__(self, ctx: Dict[str, Any]):
        self.ctx: Dict[str, Any] = ctx

    def error(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logging_logger.error(self._print_log(message, ctx))

    def warn(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logging_logger.warning(self._print_log(message, ctx))

    def warning(self, message: str, **ctx):
        self.warn(message, **ctx)

    def info(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logging_logger.info(self._print_log(message, ctx))

    def debug(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logging_logger.debug(self._print_log(message, ctx))

    def _print_log(self, message: str, ctx: Dict[str, Any]) -> str:
        merged_context = {**self.ctx, **ctx}
        display_context = _display_context(merged_context)
        if display_context:
            return f'{message} {display_context}'
        else:
            return message
        
    def exception(self, e: BaseException):
        log_exception(e)
        
    def contextualize(self, **ctx) -> 'ContextLogger':
        merged_context = {**self.ctx, **ctx}
        return ContextLogger(merged_context)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


"""Root logger"""
logger = ContextLogger(dict())
log = logger  # Deprecated alias


def log_exception(e: BaseException):
    """
    Log exception in concise one-line format containing message, exception type and short traceback
    """
    error_msg, ctx = extended_exception_details(e)
    logger.error(error_msg, **ctx)


@contextmanager
def add_context(context_name: str, log: bool = False, **ctx):
    """Apply context to occurred errors and propagate them further"""
    if log:
        logger.debug(context_name)
    try:
        yield
    except ContextError as e:
        merged_context = {**ctx, **e.ctx}
        raise ContextError(context_name, **merged_context) from e
    except BaseException as e:
        raise ContextError(context_name, **ctx) from e


class ColoredFormatter(logging.Formatter):
    def __init__(self, plain_formatter):
        logging.Formatter.__init__(self)
        self.plain_formatter = plain_formatter

    log_level_templates = {
        'CRITICAL': f'{Style.BRIGHT + Fore.RED}CRIT {Style.RESET_ALL}',
        'ERROR': f'{Style.BRIGHT + Fore.RED}ERROR{Style.RESET_ALL}',
        'WARNING': f'{Fore.YELLOW}WARN {Style.RESET_ALL}',
        'INFO': f'{Fore.BLUE}INFO {Style.RESET_ALL}',
        'DEBUG': f'{Fore.GREEN}DEBUG{Style.RESET_ALL}',
    }

    def format(self, record: logging.LogRecord):
        if record.levelname in self.log_level_templates:
            record.levelname = self.log_level_templates[record.levelname].format(record.levelname)
        return self.plain_formatter.format(record)


def _get_logging_level(str_level: str) -> int:
    return {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL,
        'off': logging.NOTSET,
    }[str_level.lower()]


def _display_context(ctx: Dict[str, Any]) -> str:
    if len(ctx) == 0:
        return ''
    keys = ctx.keys()
    parts = [_display_context_var(key, ctx[key]) for key in keys]
    return " ".join(parts)


def _display_context_var(var: str, val: str) -> str:
    val = str(val)
    if ' ' in val:
        return f'{Fore.GREEN}{var}="{Style.BRIGHT}{val}{Style.RESET_ALL}{Fore.GREEN}"{Style.RESET_ALL}'
    else:
        return f'{Fore.GREEN}{var}={Style.BRIGHT}{val}{Style.RESET_ALL}'
