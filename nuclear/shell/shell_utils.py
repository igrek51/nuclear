import io
import subprocess
import sys
from pathlib import Path
from typing import Optional

from nuclear.sublog.logging import logger


def shell(
    cmd: str, 
    workdir: Optional[Path] = None,
    print_stdout: bool = False,
    print_log: bool = False,
    raw_output: bool = False,
    independent: bool = False,
    output_file: Optional[Path] = None,
) -> str:
    """
    Run system shell command and return its output.
    Print live stdout in real time (line by line) and capture output in case of errors.
    :param cmd: shell command to run
    :param workdir: working directory for the command
    :param print_stdout: whether to print live stdout in real time (line by line) from a subprocess
    :param print_log: whether to print a log message about running the command
    :param raw_output: whether to let subprocess manage stdout/stderr on its own instead of capturing it
    :param independent: whether to start an independent process that can outlive the caller process
    :param output_file: optional file to write the output in real time
    :return: stdout of the command combined with stderr
    :raises:
        CommandError: in case of non-zero command exit code
    """
    output_file_writer = open(output_file, 'a') if output_file else None

    popen_kwargs = {
        'shell': True,
        'cwd': workdir,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
    }
    if independent:
        popen_kwargs['start_new_session'] = True
    if raw_output:
        popen_kwargs['stdout'] = None
        popen_kwargs['stderr'] = None

    process = subprocess.Popen(cmd, **popen_kwargs)
    if print_log:
        if independent:
            logger.debug('Starting process', cmd=cmd, pid=process.pid)
        else:
            logger.debug(f'Command: {cmd}')

    try:
        if raw_output:
            process.wait()
            if process.returncode != 0:
                raise CommandError(cmd, '', process.returncode)
            return ''
        
        captured_stream = io.StringIO()
        for line in iter(process.stdout.readline, b''):
            line_str = line.decode()
            if print_stdout:
                sys.stdout.write(line_str)
                sys.stdout.flush()
            if output_file_writer is not None:
                output_file_writer.write(line_str)
            captured_stream.write(line_str)

        process.wait()
        if output_file_writer is not None:
            output_file_writer.close()
        if process.returncode != 0:
            stdout = captured_stream.getvalue()
            raise CommandError(cmd, stdout, process.returncode)
        return captured_stream.getvalue()
    except KeyboardInterrupt:
        if not independent:
            logger.warning('killing subprocess', pid=process.pid)
            process.kill()
        raise


class CommandError(RuntimeError):
    def __init__(self, cmd: str, stdout: str, return_code: int):
        super().__init__()
        self.cmd = cmd
        self.stdout = stdout
        self.return_code = return_code

    def __str__(self):
        return f'command failed: {self.cmd}: {self.stdout}'


class ShellExecutor:
    """An instance for running shell commands with short syntax: sh+'command'"""
    def __call__(self, cmd: str) -> str:
        return shell(cmd)

    def __add__(self, other: str) -> str:
        return shell(other)


sh = ShellExecutor()

shell_output = shell  # Deprecated alias
