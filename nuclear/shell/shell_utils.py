import io
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

from nuclear.sublog.context_logger import log


def shell(
    cmd: str, 
    workdir: Optional[Path] = None,
    print_stdout: bool = True,
    output_file: Optional[Path] = None,
):
    """
    Run system shell command.
    Print live stdout in real time (line by line) and capture output in case of errors.
    :param cmd: shell command to run
    :param workdir: working directory for the command
    :param print_stdout: whether to print live stdout in real time (line by line) from a subprocess
    :param output_file: optional file to write the output in real time
    :raises:
        CommandError: in case of non-zero command exit code
    """
    _run_shell_command(cmd, workdir, print_stdout, output_file)


def shell_output(
    cmd: str, 
    workdir: Optional[Path] = None,
    print_stdout: bool = False,
    output_file: Optional[Path] = None,
    as_bytes: bool = False,
) -> Union[str, bytes]:
    """
    Run system shell command and return its output.
    :param cmd: shell command to run
    :param workdir: working directory for the command
    :param print_stdout: whether to print live stdout in real time (line by line) from a subprocess
    :param output_file: optional file to write the output in real time
    :param as_bytes: whether to return output as bytes (or as a string)
    :return: stdout of the command
    :raises:
        CommandError: in case of non-zero command exit code
    """
    captured_stream = _run_shell_command(cmd, workdir, print_stdout, output_file)
    output: str = captured_stream.getvalue()
    if as_bytes:
        return output.encode()
    else:
        return output


def shell_error_code(
    cmd: str,
    workdir: Optional[Path] = None,
    print_stdout: bool = False,
) -> int:
    """
    Run system shell command and return its exit code.
    :param cmd: shell command to run
    :param workdir: working directory for the command
    :param print_stdout: whether to print live stdout in real time (line by line) from a subprocess
    :return: exit code of the command
    """
    try:
        _run_shell_command(cmd, workdir, print_stdout)
        return 0
    except CommandError as e:
        return e.return_code


def _run_shell_command(
    cmd: str, 
    workdir: Optional[Path], 
    print_stdout: bool,
    output_filename: Optional[Path] = None,
) -> io.StringIO:
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT, cwd=workdir)
    output_file = open(output_filename, 'a') if output_filename else None
    try:
        captured_stream = io.StringIO()
        for line in iter(process.stdout.readline, b''):
            line_str = line.decode()
            if print_stdout:
                sys.stdout.write(line_str)
                sys.stdout.flush()
            if output_file is not None:
                output_file.write(line_str)
            captured_stream.write(line_str)

        process.wait()
        if output_file is not None:
            output_file.close()
        if process.returncode != 0:
            stdout = captured_stream.getvalue()
            raise CommandError(cmd, stdout, process.returncode)
        return captured_stream
    except KeyboardInterrupt:
        process.kill()
        raise


class CommandError(RuntimeError):
    def __init__(self, cmd: str, stdout: str, return_code: int):
        super().__init__()
        self.cmd = cmd
        self.stdout = stdout
        self.return_code = return_code

    def __str__(self):
        return f'command error: {self.cmd}: {self.stdout}'
