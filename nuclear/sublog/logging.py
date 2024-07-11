from contextlib import contextmanager
from datetime import datetime, timezone
import logging
import json
import os
import sys
import threading
import time
from typing import Dict, Any, Callable, List, Optional

from colorama import init, Fore, Style

from nuclear.sublog.context_error import ContextError
from nuclear.sublog.exception import extended_exception_details
from nuclear.utils.collections import coalesce
from nuclear.utils.env import is_env_flag_enabled
from nuclear.utils.strings import strip_ansi_colors

LOG_FORMAT = f'{Style.DIM}[%(asctime)s]{Style.RESET_ALL} %(levelname)s %(message)s'
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
LOG_DATE_FORMAT_UTC = r'%Y-%m-%d %H:%M:%SZ'
ISO_DATE_FORMAT = r'%Y-%m-%dT%H:%M:%S.%fZ'
LOGGING_LOGGER_NAME = 'nuclear.sublog'

simultaneous_print_lock = threading.Lock()
_logging_logger: logging.Logger = logging.getLogger(LOGGING_LOGGER_NAME)
_log_state = {'init': False}


def init_logs(
    show_time: Optional[bool] = None,
    show_log_level: Optional[bool] = None,
):
    """
    Configure loggers: formatters, handlers and log levels
    :param show_time: True to display formatted time in each log message,
    False to turn it off, None to use the default
    :param show_log_level: True to display log level in each log message,
    False to turn it off, None to use the default
    """
    logging_kwargs: Dict[str, Any] = {
        'stream': sys.stdout,
        'format': LOG_FORMAT,
        'level': logging.INFO,
        'datefmt': LOG_DATE_FORMAT,
    }
    if sys.version_info[1] >= 8:
        logging_kwargs['force'] = True
    if is_env_flag_enabled('NUCLEAR_STRUCTURED_LOGGING', 'false'):
        logging_kwargs['datefmt'] = ISO_DATE_FORMAT
        logging.basicConfig(**logging_kwargs)
        for handler in logging.getLogger().handlers:
            handler.setFormatter(StructuredFormatter())
    else:
        _show_log_time: bool = coalesce(show_time, is_env_flag_enabled('NUCLEAR_LOG_TIME', 'true'))
        _show_log_level: bool = coalesce(show_log_level, is_env_flag_enabled('NUCLEAR_LOG_LEVEL_SHOW', 'true'))
        logging.basicConfig(**logging_kwargs)
        for handler in logging.getLogger().handlers:
            handler.setFormatter(ColoredFormatter(_show_log_time, _show_log_level))

    log_level: str = os.environ.get('NUCLEAR_LOG_LEVEL', 'debug')
    level = _get_logging_level(log_level)
    root_logger = logging.getLogger(LOGGING_LOGGER_NAME)
    root_logger.setLevel(level)
    _log_state['init'] = True


def init_logs_once():
    if not _log_state['init']:
        init_logs()


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
        self.structured_logging: bool = is_env_flag_enabled('NUCLEAR_STRUCTURED_LOGGING', 'false')
        self.first_use = True

    def error(self, message: str, **ctx):
        with simultaneous_print_lock:
            self._print_log(message, ctx, _logging_logger.error)

    def warning(self, message: str, **ctx):
        with simultaneous_print_lock:
            self._print_log(message, ctx, _logging_logger.warning)

    def warn(self, message: str, **ctx):
        self.warning(message, **ctx)

    def info(self, message: str, **ctx):
        with simultaneous_print_lock:
            self._print_log(message, ctx, _logging_logger.info)

    def debug(self, message: str, **ctx):
        with simultaneous_print_lock:
            self._print_log(message, ctx, _logging_logger.debug)

    def _print_log(self, message: str, ctx: Dict[str, Any], logger_func: Callable):
        if self.first_use and not _log_state['init']:
            init()
            init_logs()
            self.first_use = False

        merged_context = {**self.ctx, **ctx}
        if self.structured_logging:
            logger_func(message, extra={'extra': merged_context})
        else:
            display_context = _display_context(merged_context)
            if display_context:
                if message.endswith(':'):
                    message = message[:-1]
                logger_func(f'{message}, {display_context}')
            else:
                logger_func(message)
        
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
        logger.debug(context_name, **ctx)
    try:
        yield
    except ContextError as e:
        merged_context = {**ctx, **e.ctx}
        raise ContextError(context_name, **merged_context) from e
    except BaseException as e:
        raise ContextError(context_name, **ctx) from e


class ColoredFormatter(logging.Formatter):
    def __init__(self, log_time_show: bool, log_level_show: bool):
        logging.Formatter.__init__(self)
        self.log_level_show: bool = log_level_show
        self.log_time_show: bool = log_time_show

    log_level_templates = {
        'CRITICAL': f'{Style.BRIGHT + Fore.RED}CRIT {Style.RESET_ALL}',
        'ERROR': f'{Style.BRIGHT + Fore.RED}ERROR{Style.RESET_ALL}',
        'WARNING': f'{Fore.YELLOW}WARN {Style.RESET_ALL}',
        'INFO': f'{Fore.BLUE}INFO {Style.RESET_ALL}',
        'DEBUG': f'{Fore.GREEN}DEBUG{Style.RESET_ALL}',
    }

    def format(self, record: logging.LogRecord) -> str:
        parts: List[str] = []
        part_time = self.format_time()
        if part_time:
            parts.append(part_time)
        if self.log_level_show:
            part_levelname = self.log_level_templates.get(record.levelname, record.levelname)
            parts.append(part_levelname)
        log_message: str = record.getMessage()
        parts.append(log_message)
        line = ' '.join(parts)
        if not sys.stdout.isatty():
            line = strip_ansi_colors(line)
        return line
    
    def format_time(self) -> Optional[str]:
        if not self.log_time_show:
            return None
        now_tz = datetime.now().astimezone()
        if time.timezone == 0:
            time_formatted = now_tz.strftime(LOG_DATE_FORMAT_UTC)
        else:
            time_formatted = now_tz.strftime(LOG_DATE_FORMAT)
        return f'{Style.DIM}[{time_formatted}]{Style.RESET_ALL}'


class StructuredFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record: logging.LogRecord) -> str:
        timestamp: float = record.created
        time: str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(ISO_DATE_FORMAT)
        level: str = record.levelname
        message: str = strip_ansi_colors(record.msg)
        extra = record.__dict__.get('extra', {})
        log_rec = {
            "time": time,
            "level": level,
            "message": message,
            **extra,
        }
        return json.dumps(log_rec)


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
