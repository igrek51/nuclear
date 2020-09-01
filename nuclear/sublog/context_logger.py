import datetime
import threading
from contextlib import contextmanager
from typing import Dict, Any, Optional

from colorama import Fore, Style

simultaneous_print_lock = threading.Lock()


class ContextLogger(object):
    def __init__(self, ctx: Dict[str, Any]):
        self.ctx: Dict[str, Any] = ctx

    def error(self, message: str, **ctx):
        self._print_log(message, f'[{Fore.RED + Style.BRIGHT}ERROR{Style.RESET_ALL}]', ctx)

    def warn(self, message: str, **ctx):
        self._print_log(message, f'[{Fore.YELLOW + Style.BRIGHT}WARN{Style.RESET_ALL} ]', ctx)

    def info(self, message: str, **ctx):
        self._print_log(message, f'[{Fore.BLUE}INFO{Style.RESET_ALL} ]', ctx)

    def debug(self, message: str, **ctx):
        self._print_log(message, f'[{Fore.GREEN}DEBUG{Style.RESET_ALL}]', ctx)

    def _print_log(self, message: str, level: str, ctx: Dict[str, Any]):
        merged_context = {**self.ctx, **ctx}
        display_context = _display_context(merged_context)
        timestamp_part = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if display_context:
            to_print = f'[{Fore.CYAN}{timestamp_part}{Style.RESET_ALL}] {level} {message} {display_context}'
        else:
            to_print = f'[{Fore.CYAN}{timestamp_part}{Style.RESET_ALL}] {level} {message}'
        with simultaneous_print_lock:
            print(to_print)

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
