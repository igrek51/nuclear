import threading
from contextlib import contextmanager
from typing import Dict, Any, Optional
import logging
import sys

from colorama import Fore, Style

simultaneous_print_lock = threading.Lock()

LOG_FORMAT = f'{Style.DIM}[%(asctime)s]{Style.RESET_ALL} %(levelname)s %(message)s'
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'


def _init_logger(log_level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger('nuclear.sublog')
    logger.setLevel(log_level)
    logger.propagate = False

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(ColoredFormatter(formatter))
    logger.addHandler(handler)
    return logger


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


_logger = _init_logger()


def get_logger(logger_name: Optional[str] = None) -> logging.Logger:
    """
    Get configured logger
    :param logger_name: Name of the child logger. It's best to keep it __name__
    """
    logger = logging.getLogger('nuclear.sublog')
    if logger_name:
        return logger.getChild(logger_name)
    return logger


class ContextLogger(object):
    def __init__(self, ctx: Dict[str, Any]):
        self.ctx: Dict[str, Any] = ctx

    def error(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logger.error(self._print_log(message, ctx))

    def warn(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logger.warning(self._print_log(message, ctx))

    def warning(self, message: str, **ctx):
        self.warn(message, **ctx)

    def info(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logger.info(self._print_log(message, ctx))

    def debug(self, message: str, **ctx):
        with simultaneous_print_lock:
            _logger.debug(self._print_log(message, ctx))

    def _print_log(self, message: str, ctx: Dict[str, Any]) -> str:
        merged_context = {**self.ctx, **ctx}
        display_context = _display_context(merged_context)
        if display_context:
            return f'{message} {display_context}'
        else:
            return message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


"""Root logger"""
log = ContextLogger(dict())


def context_logger(parent: Optional[ContextLogger] = None, **ctx) -> ContextLogger:
    if parent is None:
        return ContextLogger(ctx)
    else:
        merged_context = {**parent.ctx, **ctx}
        return ContextLogger(merged_context)


@contextmanager
def root_context_logger(**ctx) -> ContextLogger:
    ctx_backup: Dict[str, Any] = log.ctx
    try:
        log.ctx = {**ctx_backup, **ctx}
        yield log
    finally:
        log.ctx = ctx_backup


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
