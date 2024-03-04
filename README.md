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
- [WAT](https://igrek51.github.io/nuclear/inspect/) - inspection tool
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

You need Python 3.8 or newer.


# 🙀 WAT Inspector

**Nuclear** comes with a powerful inspection tool
that allows you to delve into and examine unknown objects at runtime.

> "Wat" is a variant of the English word "what" that is often used to express confusion or disgust

If you find yourself deep within the Python console, feeling dazed and confused,
wondering "WAT? What's that thing?",
that's where the `wat` inspector comes in handy.

Start the Python Interpreter (or attach to your program) and execute `wat(object)` on any `object`
to investigate its
**type**, **formatted value**, **variables**, **methods**, **parent types**, **signature**,
**documentation**, and even its **source code**.

<video width="100%" controls="true" allowfullscreen="true" src="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect.mp4" poster="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect-poster.png">
</video>

## Import
Import inspection tools from **nuclear** package.
```sh
pip install nuclear
```
```python
from nuclear import wat
```

Alternatively, use **Insta-Load** in the section below.

### Insta-Load
If you want to debug something quickly,
you don't even need to install **nuclear** package to use `wat` inspector.

Load it on the fly by pasting this snippet to your Python interpreter:
```python
import base64, zlib
code = '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'
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
```

Now you can use `wat`.

## Usage & modifiers
Nuclear comes with the `wat` object that can quickly inspect things
by using the division operator (to avoid typing parentheses). 
A short, no-parentheses syntax `wat / object` is equivalent to `wat(object)`.

You can call `wat.modifiers / object` (or `wat.modifiers(object)`)
with the following **modifiers**:

- `.short` to hide attributes (variables and methods)
- `.long` to show non-abbreviated values and documentation
- `.dunder` to display dunder attributes
- `.code` to reveal the source code of a function, method, or class
- `.nodocs` to hide documentation for functions and classes
- `.all` to include all available information

You can chain modifiers, e.g. `wat.long.dunder / object`.

Call `wat()` to inspect `locals()` variables.

Type `wat` in the interpreter to learn more about this object itself.

## Use cases

### Determine type
In a dynamic typing language like Python, it's often hard to determine the type of an object. WAT Inspector can help you with that by showing the name of the type with the module it comes from.

```python
>>> wat.short({None})
value: {None}
type: set
len: 1
```

```python
>>> wat.short / user
str: admin
repr: <User: admin>
type: django.contrib.auth.models.User
parents: django.contrib.auth.models.AbstractUser, django.contrib.auth.base_user.AbstractBaseUser, django.contrib.auth.models.PermissionsMixin, django.db.models.base.Model, django.db.models.utils.AltersData
```

### Look up methods
Listing methods, functions and looking up their signature is extremely beneficial to see how to use them.
Plus, you can read their docstrings.

```python
wat('stringy')
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-string.png?raw=true)

### Discover function's signature
See the docstrings and the signature of a function or a method to see how to use it.

```python
wat(str.split)
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-str-split.png?raw=true)

### Look up variables
Check what's inside, list the value of variables and their types to see what's really inside the inspected object.
```python
wat / re.match('(\d)_(.*)', '1_title')
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-re-match.png?raw=true)

### Explore modules
One of the use cases is to explore modules.
For instance you can list functions, classes and the sub-modules of a selected module.

```python
import pathlib
wat / pathlib
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-pathlib.png?raw=true)

Then, you can navigate further, e.g. `wat / pathlib.fnmatch`.

### Explore dunder attributes
```python
wat.dunder / {}
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-dict-dunder.png?raw=true)

### Review the code
Look up the source code of a function to see how it really works.

```python
import re
wat.code / re.match
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-code-rematch.png?raw=true)

### Debug with breakpoint
You can use Python's `breakpoint()` keyword to launch an interactive debugger in your program:

```python
logger.debug('init')
x = {'what is it?'}
breakpoint()
logger.debug('done')
```

```python
(Pdb) from nuclear import wat  # or paste insta-load snippet
(Pdb) wat / x  # inspect local variable
...
(Pdb) c  # continue execution
```

### Explore Python built-ins
```python
wat / __builtins__
```

### Look up local variables
```python
wat()
```


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
