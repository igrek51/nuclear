import subprocess
from typing import Union

from .output import fatal


def shell(cmd: str):
    err_code = shell_error_code(cmd)
    if err_code != 0:
        fatal('failed executing: %s' % cmd)


def shell_error_code(cmd: str) -> int:
    return subprocess.call(cmd, shell=True)


def shell_output(cmd: str, as_bytes: bool = False) -> Union[str, bytes]:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    if as_bytes:
        return output
    else:
        return output.decode('utf-8')
