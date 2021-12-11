# Nuclear - binding glue for CLI
[![GitHub version](https://badge.fury.io/gh/igrek51%2Fnuclear.svg)](https://github.com/igrek51/nuclear)
[![PyPI version](https://badge.fury.io/py/nuclear.svg)](https://pypi.org/project/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://app.travis-ci.com/igrek51/nuclear.svg?branch=master)](https://app.travis-ci.com/igrek51/nuclear)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)
[![Github Pages](https://img.shields.io/badge/github.io-ok-brightgreen)](https://igrek51.github.io/nuclear)


`nuclear` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

`nuclear` parses and validates the command line arguments provided by the user when starting a console application.
It then automatically invokes the appropriate action, based on the declared Command-Line Interface rules, injecting all the necessary  parameters.
You don't need to write the "glue" code to bind & parse the parameters each time.
This makes writing console aplications simpler and clearer.

## Demo
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument, flag, parameter, subcommand

CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        parameter('repeat', type=int, default=1),
        flag('decode', help='Decode name as base64'),
    ),
    subcommand('calculate').has(
        subcommand('factorial', run=calculate_factorial,
                    help='Calculate factorial').has(
            argument('n', type=int),
        ),
        subcommand('primes', run=calculate_primes,
                    help='List prime numbers using Sieve of Eratosthenes').has(
            argument('n', type=int, required=False, default=100,
                        help='maximum number to check'),
        ),
    ),
).run()
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-live.gif?raw=true)

See [demo.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo.py) for a complete example
or [demo-decorator.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-decorator.py)
(if you want to do the same using decorator-based syntax).

## Get it now
```bash
pip install nuclear
```

## Table of contents - Our chief weapons are...
- [Auto-generated help and usage](https://nuclear-py.readthedocs.io/en/latest/help) (`--help`)
- [Multilevel Sub-commands](https://nuclear-py.readthedocs.io/en/latest/subcommands) (e.g. `git remote add ...` syntax)
- [Flags](https://nuclear-py.readthedocs.io/en/latest/flags): supporting both short (`-f`) and long (`--force`), combining short flags (`-tulpn`), multiple flag occurrences (`-vvv`)
- [Named parameters](https://nuclear-py.readthedocs.io/en/latest/parameters): supporting both `--name value` and `--name=value`, multiple parameter occurrences
- [Positional arguments](https://nuclear-py.readthedocs.io/en/latest/positional-args) (e.g. `git push <origin> <master>`)
- [Many positional arguments](https://nuclear-py.readthedocs.io/en/latest/many-args) (e.g. `docker run cmd ubuntu </bin/bash -c /script.sh>`)
- [Key-value dictionaries](https://nuclear-py.readthedocs.io/en/latest/dictionaries) (e.g. `--config key value`)
- [Logging with sublog](https://nuclear-py.readthedocs.io/en/latest/sublog)
- [Shell Auto-completion](https://nuclear-py.readthedocs.io/en/latest/autocompletion) (getting most relevant hints on hitting `Tab`)
- [Custom auto-completers](https://nuclear-py.readthedocs.io/en/latest/autocompletion/#custom-completers) (providers of possible values)
- [Parsing data types](https://nuclear-py.readthedocs.io/en/latest/data-types) (int, boolean, time, date, file, etc.)
- [CLI Builder](https://nuclear-py.readthedocs.io/en/latest/builder)
- [Custom type validators / parsers](https://nuclear-py.readthedocs.io/en/latest/data-types/#custom-type-parsers)
- [Errors handling](https://nuclear-py.readthedocs.io/en/latest/errors)
- [Quick start](https://nuclear-py.readthedocs.io/en/latest/quick-start/)
- [How does it work?](https://nuclear-py.readthedocs.io/en/latest/how-it-works/)
- [Nuclear vs argparse](https://nuclear-py.readthedocs.io/en/latest/vs-argparse)
- [Installation](https://nuclear-py.readthedocs.io/en/latest/installation)
- [CLI Rules cheatsheet](https://nuclear-py.readthedocs.io/en/latest/cheatsheet)

## How does it work?
1. You define CLI rules for your program in a declarative tree using `CliBuilder`. Rules can bind your functions to be called later.
2. When running your program in a shell provided with command-line arguments, it starts `.run()` which does the parsing.
3. `nuclear` parses and validates all the parameters, flags, sub-commands, positional arguments, etc., and stores them internally.
4. `nuclear` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `nuclear` injects all its needed parameters based on the previously defined & parsed values.

You just need to bind the keywords with rules and `nuclear` will take care of the rest for you.

## Quick start
Let's create a simple command-line application using `nuclear`.
Let's assume we already have our fancy functions as follows:
```python
def say_hello(name: str, decode: bool, repeat: int):
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))

def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))
```
and we need a "glue" which binds them with a CLI (Command-Line Interface).
We want it to be run with different keywords and parameters provided by user to the terminal shell in a following manner:
- `./quickstart.py hello NAME --decode --repeat=3` mapped to `say_hello` function,
- `./quickstart.py calculate factorial N` mapped to `calculate_factorial` function,
- `./quickstart.py calculate primes N` mapped to `calculate_primes` function,

We've just identified 2 main commands in a program: `hello` and `calculate` (which in turn contains 2 subcommands: `factorial` & `primes`). That forms a tree:
- `hello` command has one positional argument `NAME`, one boolean flag `decode` and one numerical parameter `repeat`.
- `calculate` command has 2 another subcommands:
    * `factorial` subcommand has one positional argument `N`,
    * `primes` subcommand has one positional argument `N`,

So our CLI definition may be declared using `nuclear` in a following way:
```python
CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        parameter('repeat', type=int, default=1),
        flag('decode', help='Decode name as base64'),
    ),
    subcommand('calculate').has(
        subcommand('factorial', run=calculate_factorial,
                    help='Calculate factorial').has(
            argument('n', type=int),
        ),
        subcommand('primes', run=calculate_primes,
                    help='List prime numbers using Sieve of Eratosthenes').has(
            argument('n', type=int, required=False, default=100,
                        help='maximum number to check'),
        ),
    ),
)
```

Getting it all together, we've bound our function with a Command-Line Interface:

**quickstart.py**:
```python
#!/usr/bin/env python3
import base64
from functools import reduce
from nuclear import CliBuilder, argument, flag, parameter, subcommand

def say_hello(name: str, decode: bool, repeat: int):
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))

def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))

CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        flag('decode', help='Decode name as base64'),
        parameter('repeat', type=int, default=1),
    ),
    subcommand('calculate').has(
        subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
            argument('n', type=int),
        ),
        subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
            argument('n', type=int, required=False, default=100, help='maximum number to check'),
        ),
    ),
).run()
```

Let's trace what is happening here:

- `CliBuilder()` builds CLI tree for entire application.
- `.has(...)` allows to embed other nested rules inside that builder. Returns `CliBuilder` itself for further building.
- `subcommand('hello', run=say_hello)` binds `hello` command to `say_hello` function. From now, it will be invoked when `hello` command occurrs.
- `subcommand.has(...)` embeds nested subrules on lower level for that subcommand only.
- `argument('name')` declares positional argument. From now, first CLI argument (after binary name and commands) will be recognized as `name` variable.
- `flag('decode')` binds `--decode` keyword to a flag named `decode`. So as it may be used later on. Providing `help` adds description to help screen.
- `parameter('repeat', type=int, default=1)` binds `--repeat` keyword to a parameter named `repeat`, which type is `int` and its default value is `1`.
- Finally, invoking `.run()` does all the magic.
It gets system arguments list, starts to process them and invokes most relevant action.

### Decorator builder
We can do the same using decorator-based syntax, which binds the functions to the CLI:
```python
cli = CliBuilder()

@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """Say hello to someone"""
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))


@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))


@cli.add_command('calculate', 'primes')
def calculate_primes(n: int = 100):
    """List prime numbers using Sieve of Eratosthenes"""
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))

if __name__ == '__main__':
    cli.run()
```

### Help / Usage
`CliBuilder` has some basic options added by default, e.g. `--help`.
Thus, you can check the usage by running application with `--help` flag:
```console
foo@bar:~$ ./quickstart.py --help
Usage:
./quickstart.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...] - Display this help and exit

Commands:
  hello NAME           
  calculate factorial N - Calculate factorial
  calculate primes [N]  - List prime numbers using Sieve of Eratosthenes

Run "./quickstart.py COMMAND --help" for more information on a command.
```

As prompted, we can check more detailed subcommand helps:
```console
foo@bar:~$ ./quickstart.py hello --help
Usage:
./quickstart.py hello [OPTIONS] NAME

Arguments:
   NAME

Options:
  --decode                    - Decode name as base64
  --repeat REPEAT             - Default: 1
  -h, --help [SUBCOMMANDS...] - Display this help and exit
```

### Injecting parameters
Let's invoke `say_hello` function on a first run.

Now when we execute our application with required argument provided, we get:
```console
foo@bar:~$ ./quickstart.py hello world
I'm a world!
```
Note that `world` has been recognized as `name` argument.
We've binded `say_hello` as a default action, so it has been invoked with particular parameters:
```python
say_hello(name='world', decode=False, repeat=1)
```

- positional argument `name` has been assigned a `'world'` value.
- flag `decode` was not given, so it's `False` by default.
- parameter `repeat` was not given either, so it was set to its default value `1`.

Let's provide all of the parameters explicitly, then we get:
```console
foo@bar:~$ ./quickstart.py hello UGlja2xl --decode --repeat=3
I'm a Pickle! I'm a Pickle! I'm a Pickle!
```
Or we can do the same in arbitrary order:
```console
foo@bar:~$ ./quickstart.py hello --repeat 3 --decode UGlja2xl
I'm a Pickle! I'm a Pickle! I'm a Pickle!
```

Invoking other subcommands is just as easy:
```console
foo@bar:~$ ./quickstart.py calculate primes 50
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49]
```

When you are writing function for your action and you need to access some of the variables (flags, parameters, arguments, etc.),
just simply add a parameter to the function with a name same as the variable you need.
Then, the proper value will be parsed and injected by `nuclear`.

## `nuclear` vs `argparse`
Why use `nuclear`, since Python already has `argparse`? Here are some subjective advantages of `nuclear`:

- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building - when reading the code, it's easier to distinguish particular CLI rules between them (i.e. flags from positional arguments, parameters or sub-commands),
- CLI definition code as a clear documentation.

Sub-commands done with `argparse`:
```python
def foo(args):
    print(args.x * args.y)

def bar_go(args):
    print(args.z)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

def _print_help(_: argparse.Namespace):
    parser.print_help(sys.stderr)

parser.set_defaults(func=_print_help)

parser_foo = subparsers.add_parser('foo', help='foo help')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

parser_bar = subparsers.add_parser('bar', help='"bar" help')
subparsers_bar = parser_bar.add_subparsers()

parser_bar_go = subparsers_bar.add_parser('go', help='"bar go" help')
parser_bar_go.add_argument('z')
parser_bar_go.set_defaults(func=bar_go)

args = parser.parse_args()
args.func(args)
```
with nuclear it's much simpler and cleaner:
```python
def foo(x, y):
    print(x * y)

def bar_go(z):
    print(z)


CliBuilder().has(
    subcommand('foo', help='foo help', run=foo).has(
        parameter('-x', type=int, default=1),
        argument('y', type=float),
    ),
    subcommand('bar', help='"bar" help').has(
        subcommand('go', help='"bar go" help', run=bar_go).has(
            argument('z'),
        ),
    ),
).run()
```

## Installation
### Step 1. Prerequisites
- Python 3.6 or newer (`sudo apt install python3` on Debian/Ubuntu)
- pip

### Step 2. Install package using pip
Install package from [PyPI repository](https://pypi.org/project/nuclear) using pip:
```bash
pip3 install nuclear
```

### Install package in develop mode
You can install package in develop mode in order to make any changes for your own:
```bash
pip3 install -r requirements.txt
python3 setup.py develop
```

## Testing
Running tests:
```bash
make setup
. venv/bin/activate
make test
```

## Logging with sublog
`sublog` is a logging system that allows you to:  
- display variables besides log messages: `log.debug('message', airspeed=20)`,
- wrap errors with context: `with wrap_context('ignition')`,
- catch errors and show traceback in a concise, pretty format: `with  logerr()`.

```python
from nuclear.sublog import log, logerr, wrap_context

with logerr():
    log.debug('checking engine', temperature=85.0, pressure='12kPa')
    with wrap_context('ignition', request=42):
        log.info('ignition ready', speed='zero')
        with wrap_context('liftoff'):
            raise RuntimeError('explosion')
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/img/sublog-demo.png?raw=true)

## CLI Rules cheatsheet
Here is the cheatsheet with the most important CLI rules:
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument, arguments, flag, parameter, subcommand, dictionary


def main():
    CliBuilder('hello-app', version='1.0.0', help='welcome', run=say_hello).has(
        flag('--verbose', '-v', help='verbosity', multiple=True),
        parameter('repeat', 'r', help='how many times', type=int, required=False, default=1, choices=[1, 2, 3, 5, 8]),
        argument('name', help='description', required=False, default='world', type=str, choices=['monty', 'python']),
        arguments('cmd', joined_with=' '),
        subcommand('run', help='runs something').has(
            subcommand('now', 'n', run=lambda cmd: print(f'run now: {cmd}')),
        ),
        dictionary('config', 'c', help='configuration', key_type=str, value_type=int)
    ).run()


def say_hello(name: str, verbose: int, repeat: int, cmd: str, config: dict):
    print(f'Hello {name}')


if __name__ == '__main__':
    main()
```

