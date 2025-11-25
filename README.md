# ☢️ Nuclear
[![GitHub version (latest SemVer)](https://img.shields.io/github/v/tag/igrek51/nuclear?label=github&sort=semver)](https://github.com/igrek51/nuclear)
[![PyPI](https://img.shields.io/pypi/v/nuclear)](https://pypi.org/project/nuclear)
[![Github Pages](https://img.shields.io/badge/docs-github.io-blue)](https://igrek51.github.io/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/igrek51/nuclear/test.yml?branch=master&label=tests)](https://github.com/igrek51/nuclear/actions?query=workflow%3Atest)

<div align="center">
    <a href="https://github.com/igrek51/nuclear">GitHub</a>
    -
    <a href="https://pypi.org/project/nuclear">PyPI</a>
    -
    <a href="https://igrek51.github.io/nuclear">Documentation</a>
</div>

*Nuclear* is a binding glue for CLI applications.
It consists of tools for building CLI applications in Python, including:

- [CLI parser](https://igrek51.github.io/nuclear/quick-start/) for building nested CLI commands
- [Sublog](https://igrek51.github.io/nuclear/sublog/) - contextual logger
- [Shell utilities](https://igrek51.github.io/nuclear/shell/)


# CLI Demo
```python
from nuclear import CliBuilder

cli = CliBuilder()

@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """
    Say hello
    :param decode: Decode name as base64
    """
    message = f"I'm a {b64decode(name).decode() if decode else name}!"
    print(' '.join([message] * repeat))

@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

@cli.add_command('calculate', 'primes')
def calculate_primes(n: int):
    """List prime numbers using Sieve of Eratosthenes"""
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), range(2, n), set(range(2, n)))))

cli.run()
```

![](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-live.gif?raw=true)

See [demo.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-decorator.py) for a complete example.

# Installation
```bash
python3 -m pip install --upgrade nuclear
```

You need Python 3.10 or newer.


# 📜 Sublog
**Sublog** is a *nuclear*'s contextual logging system that allows you to:
  
- display variables besides log messages: `logger.debug('message', airspeed=20)`,
- wrap errors with context: `with add_context('ignition')`,
- catch errors and show traceback in a concise, pretty format: `with error_handler()`.

```python
from nuclear.sublog import logger, error_handler, add_context

with error_handler():
    logger.debug('checking engine', temperature=85.0, pressure='12kPa')
    with add_context('ignition', request=42):
        logger.info('ignition ready', speed='zero')
        with add_context('liftoff'):
            raise RuntimeError('explosion')
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/img/sublog-demo.png?raw=true)

## Context logger
Use `nuclear.sublog.logger` to log message with a pretty format out of the box.

Pass additional context variables as keyword arguments to display them in the log message.

```python
from nuclear.sublog import logger

logger.info('info log')
logger.debug('debug log', var1=1, var2='two')
logger.info('not great not terrible', radioactivity=3.6)
logger.error('this is bad')
logger.exception(RuntimeError('this is worse'))
```

## Error handler
Use `nuclear.sublog.error_handler` to catch errors and show traceback in a concise, pretty format.

```python
from nuclear.sublog import error_handler

with error_handler():
    raise RuntimeError('explosion')
```

## Wrapping context
Use `nuclear.sublog.add_context` to wrap code with additional context information.
This will be included in in the log message, if an error occurs.

```python
from nuclear.sublog import add_context

with add_context('reloading plugins'):
    with add_context('loading config'):
        raise RuntimeError('file is missing')
```
This will produce an error with the following message:
```
reloading plugins: loading config: file is missing
```

Note that while each individual part of the message may not provide a comprehensive explanation of the error,
when combined, the whole message becomes highly informative.
This is the core principle behind enriching errors with context.


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
