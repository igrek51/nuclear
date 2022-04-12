import io
import os
import select
import shlex
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Union

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


class BackgroundCommand:
    def __init__(self,
        cmd: str,
        on_next_line: Callable[[str], None] = None,
        on_error: Callable[[CommandError], None] = None,
        print_stdout: bool = False,
        debug: bool = False,
        shell: bool = True,
    ):
        """Run system shell command in background."""
        self._stop: bool = False
        self._captured_stream = io.StringIO()

        def monitor_output(stream: BackgroundCommand):
            stdout_iter = iter(stream._process.stdout.readline, b'')
            poll_obj = select.poll()
            poll_obj.register(self._process.stdout, select.POLLIN)

            while True:
                if stream._stop:
                    break
                poll_result = poll_obj.poll(0)
                if not poll_result:
                    time.sleep(1)
                    continue

                try:
                    line = next(stdout_iter)
                except StopIteration:
                    break
                line_str = line.decode()
                if print_stdout:
                    sys.stdout.write(line_str)
                    sys.stdout.flush()
                if on_next_line is not None:
                    on_next_line(line_str)
                self._captured_stream.write(line_str)

            stream._process.wait()
            if stream._process.returncode != 0 and on_error is not None and not self._stop:
                stdout = self._captured_stream.getvalue()
                on_error(CommandError(cmd, stdout, stream._process.returncode))

            if debug:
                log.debug(f'Command finished: {cmd}')

        self._monitor_thread = threading.Thread(
            target=monitor_output,
            args=(self,),
            daemon=True,
        )

        if debug:
            log.debug(f'Command: {cmd}')
        if shell:
            process_args = cmd
        else:
            process_args = shlex.split(cmd)
            
        self._process = subprocess.Popen(
            process_args, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            shell=shell,
            preexec_fn=os.setsid,
        )

        self._monitor_thread.start()

    def terminate(self):
        self._stop = True
        self._process.terminate()
        self._process.poll()  # wait for subprocess
        self._monitor_thread.join()  # wait for thread is finished

    def wait(self):
        self._process.poll()
        self._monitor_thread.join()  # wait for thread is finished

    @property
    def stdout(self) -> str:
        return self._captured_stream.getvalue()

    @property
    def is_running(self) -> bool:
        return self._monitor_thread.is_alive()
