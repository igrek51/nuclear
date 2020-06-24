import datetime
from contextlib import contextmanager
from typing import Dict, Any, Optional

C_RESET = '\033[0m'
C_GREEN = '\033[0;32m'
C_BLUE = '\033[0;34m'
C_CYAN = '\033[0;36m'
C_RED_BOLD = '\033[1;31m'
C_GREEN_BOLD = '\033[1;32m'
C_YELLOW_BOLD = '\033[1;33m'


class ContextLogger(object):
    def __init__(self, ctx: Dict[str, Any]):
        self.ctx: Dict[str, Any] = ctx

    def error(self, message: str, **ctx):
        self._print_log(message, f'{C_RED_BOLD}ERROR{C_RESET}', ctx)

    def warn(self, message: str, **ctx):
        self._print_log(message, f'{C_YELLOW_BOLD}WARN {C_RESET}', ctx)

    def info(self, message: str, **ctx):
        self._print_log(message, f'{C_BLUE}INFO {C_RESET}', ctx)

    def debug(self, message: str, **ctx):
        self._print_log(message, f'{C_GREEN}DEBUG{C_RESET}', ctx)

    def _print_log(self, message: str, level: str, ctx: Dict[str, Any]):
        merged_context = {**self.ctx, **ctx}
        display_context = _display_context(merged_context)
        timestamp_part = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if display_context:
            print(f'[{C_CYAN}{timestamp_part}{C_RESET}] [{level}] {message} {display_context}')
        else:
            print(f'[{C_CYAN}{timestamp_part}{C_RESET}] [{level}] {message}')

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
        return f'{C_GREEN}{var}="{C_GREEN_BOLD}{val}{C_GREEN}"{C_RESET}'
    else:
        return f'{C_GREEN}{var}={C_GREEN_BOLD}{val}{C_RESET}'
