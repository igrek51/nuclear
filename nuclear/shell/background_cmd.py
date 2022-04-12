from genericpath import isdir
import io
import os
import shlex
import subprocess
import sys
import threading
import signal
from pathlib import Path
from typing import Callable, List, Optional

from nuclear.shell.shell_utils import CommandError
from nuclear.sublog.context_logger import log


class BackgroundCommand:
    def __init__(self,
        cmd: str,
        workdir: Optional[Path] = None,
        on_next_line: Callable[[str], None] = None,
        on_error: Callable[[CommandError], None] = None,
        print_stdout: bool = False,
        print_stderr: bool = True,
        shell: bool = True,
        debug: bool = False,
    ):
        """
        Run system shell command in background. Stream live stdout in real time.
        :param cmd: shell command to run
        :param workdir: working directory for the command
        :param on_next_line: callback to call on each line of stdout
        :param on_error: callback to call on command error
        :param print_stdout: whether to propagate subprocess' stdout to system stdout
        :param print_stderr: whether to capture stderr from a subprocess
        :param shell: whether to run the command with a shell parent process, ie. bash -c "cmd"
        :param debug: whether to print debug logs about running commands
        """
        self._stop: bool = False
        self._captured_stream = io.StringIO()
        self._debug = debug

        def monitor_output(stream: BackgroundCommand):
            stdout_iter = iter(stream._process.stdout.readline, b'')
            
            while True:
                if stream._stop:
                    break
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
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if print_stderr else subprocess.PIPE,
            shell=shell,
        )

        self._monitor_thread.start()

    def terminate(self):
        """Send TERMINATE signal to the process and wait until it's finished"""
        self._stop = True
        if not self._monitor_thread.is_alive():
            return

        children = _get_child_processes(self._process.pid)
        for child_pid in children:
            if self._debug:
                log.debug(f'terminating child process', pid=child_pid)
            os.kill(child_pid, signal.SIGTERM)

        self._process.terminate()
        self._process.poll()  # wait for subprocess
        if self._debug:
            log.debug(f'subprocess terminated', pid=self._process.pid)
        self._monitor_thread.join()  # wait for thread is finished

    def wait(self):
        """Wait until the process is finished"""
        self._process.poll()
        self._monitor_thread.join()  # wait for thread is finished

    @property
    def stdout(self) -> str:
        """Return captured stdout"""
        return self._captured_stream.getvalue()

    @property
    def is_running(self) -> bool:
        """Return True if the process is running"""
        return self._monitor_thread.is_alive()


def _get_child_processes(pid: int) -> List[int]:
    children_pids = []
    proc_task_path = Path(f'/proc/{pid}/task')
    if not proc_task_path.is_dir():
        log.warn(f"Can't find process task directory: {proc_task_path}")
        return []
    tasks = [t for t in proc_task_path.iterdir()]
    for task in tasks:
        task_children = task / 'children'
        if task_children.is_file():
            task_children_parts = task_children.read_text().split()
            task_pids = [int(p.strip()) for p in task_children_parts]
            children_pids.extend(task_pids)
    return children_pids
