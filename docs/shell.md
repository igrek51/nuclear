# 🐌 Shell utilities

*Nuclear* provides utilities for running system shell commands.

Basic usage:

```python
from nuclear import shell

window_id: str = shell('xdotool getactivewindow')
```

`shell` function captures the stdout & stderr output of the shell command and returns it as a string.
It may also print live stdout in real time (line by line) and capture output in case of errors.

It has a lot of possibilities thanks to its parameters:

* `cmd: str` - shell command to run
* `workdir: Optional[Path] = None` - working directory for the command
* `print_stdout: bool = False` - whether to print live stdout in real time (line by line) from a subprocess
* `print_log: bool = False` - whether to print a log message about running the command
* `raw_output: bool = False` - whether to let subprocess manage stdout/stderr on its own instead of capturing it
* `independent: bool = False` - whether to start an independent process that can outlive the caller process
* `output_file: Optional[Path] = None` - optional file to write the output in real time

It returns the stdout of the command combined with stderr.
In case of non-zero command exit code, `shell` raises `CommandError` exception.
