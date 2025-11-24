from typing import Any

from nuclear.shell.shell_utils import shell
from nuclear.sublog.logging import logger


class ShellRunner:
    def __init__(self, **shell_kwargs):
        self._shell_kwargs: dict[str, Any] = shell_kwargs
    
    def __call__(self, cmd: str, **shell_kwargs) -> str:
        return self.copy(**shell_kwargs).run(cmd)
    
    def run(self, cmd: str) -> str:
        if self._shell_kwargs.get('dry', False):
            logger.info(f'Dry command: {cmd}')
            return ''
        return shell(cmd, **self._shell_kwargs)
    
    def copy(self, **shell_kwargs) -> 'ShellRunner':
        new_shell_kwargs = self._shell_kwargs.copy()
        new_shell_kwargs.update(shell_kwargs)
        return ShellRunner(**new_shell_kwargs)

    def __truediv__(self, cmd): return self.run(cmd)  # /
    def __add__(self, cmd): return self.run(cmd)  # +
    def __lshift__(self, cmd): return self.run(cmd)  # <<
    def __rshift__(self, cmd): return self.run(cmd)  # >>
    def __or__(self, cmd): return self.run(cmd)  # sh |
    def __ror__(self, cmd): return self.run(cmd)  # | sh
    def __lt__(self, cmd): return self.run(cmd)  # <


def sh(
    raw_output: bool = False,
    dry: bool = False,
) -> ShellRunner:
    return ShellRunner(raw_output=raw_output, dry=dry)
