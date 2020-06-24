# nuclear - binding glue for CLI
[![GitHub version](https://badge.fury.io/gh/igrek51%2Fnuclear.svg)](https://github.com/igrek51/nuclear)
[![PyPI version](https://badge.fury.io/py/nuclear.svg)](https://pypi.org/project/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/igrek51/nuclear.svg?branch=master)](https://travis-ci.org/igrek51/nuclear)
[![Coverage Status](https://coveralls.io/repos/github/igrek51/nuclear/badge.svg?branch=master)](https://coveralls.io/github/igrek51/nuclear?branch=master)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)


`nuclear` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

`nuclear` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the "glue" code for binding & parsing parameters every time.
So it makes writing console aplications simpler and more clear.

## Features
- [Auto-generated help and usage](https://nuclear-py.readthedocs.io/en/latest#auto-generated-help) (`--help`)
- [Shell autocompletion](https://nuclear-py.readthedocs.io/en/latest#auto-completion) (getting most relevant hints on hitting `Tab`)
- [Multilevel sub-commands](https://nuclear-py.readthedocs.io/en/latest#sub-commands) (e.g. `git remote add ...` syntax)
- [Named parameters](https://nuclear-py.readthedocs.io/en/latest#named-parameters): supporting both `--name value` and `--name=value`, multiple parameter occurrences
- [Flags](https://nuclear-py.readthedocs.io/en/latest#flags): supporting both short (`-f`) and long (`--force`), combining short flags (`-tulpn`), multiple flag occurrences (`-vvv`)
- [Positional arguments](https://nuclear-py.readthedocs.io/en/latest#positional-arguments) (e.g. `git push <origin> <master>`)
- [Key-value dictionaries](https://nuclear-py.readthedocs.io/en/latest#dictionaries) (e.g. `--config key value`)
- [Invoking matched action function & injecting parameters](https://nuclear-py.readthedocs.io/en/latest#injecting-parameters)
- [Custom type validators / parsers](https://nuclear-py.readthedocs.io/en/latest#custom-type-parsers)
- [Custom auto-completers](https://nuclear-py.readthedocs.io/en/latest#custom-completers) (providers of possible values)
- [Handling syntax errors, parameters validation](https://nuclear-py.readthedocs.io/en/latest#errors-handling)
- [Typed values](https://nuclear-py.readthedocs.io/en/latest#data-types) (int, time, date, file, etc.)
- [Standard options](https://nuclear-py.readthedocs.io/en/latest#clibuilder) enabled by default (`--help`, `--version`)
- [Declarative CLI builder](https://nuclear-py.readthedocs.io/en/latest#cli-rules-cheatsheet)

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
    print(sorted(reduce((lambda r, x: r - set(range(x ** 2, n, x)) if (x in r) else r),
                        range(2, int(n ** 0.5)), set(range(2, n)))))
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
    print(sorted(reduce((lambda r, x: r - set(range(x ** 2, n, x)) if (x in r) else r),
                        range(2, int(n ** 0.5)), set(range(2, n)))))

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

## How does it work?
1. You define all required CLI rules for your program in a declarative tree.
2. User provides command-line arguments when running program in a shell.
3. `nuclear` parses and validates all the parameters, flags, sub-commands, positional arguments, etc, and stores them internally.
4. `nuclear` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `nuclear` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `nuclear` will handle all the rest for you.

## `nuclear` vs `argparse`
Why use `nuclear`, since Python has already `argparse`? Here are some subjective advantages of `nuclear`:

- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building - when reading the code, it's easier to distinguish particular CLI rules between them (i.e. flags from positional arguments, parameters or sub-commands),
- CLI definition code as a clear documentation.

### Migrating from `argparse` to `nuclear`

#### Migrating: Sub-commands
argparse:
```python
def foo(args):
    print(args.x * args.y)

def bar(args):
    print(args.z)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_foo = subparsers.add_parser('foo', help='foo help')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

parser_bar = subparsers.add_parser('bar', help='bar help')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=bar)

args = parser.parse_args()
args.func(args)
```
with nuclear it's much simpler and more clear:
```python
def foo(x, y):
    print(x * y)

def bar(z):
    print(z)


CliBuilder().has(
    subcommand('foo', help='foo help', run=foo).has(
        parameter('-x', type=int, default=1),
        argument('y', type=float),
    ),
    subcommand('bar', help='bar help', run=bar).has(
        argument('z'),
    ),
).run()
```

#### Migrating: Basic CLI
argparse:
```python
import argparse

parser = argparse.ArgumentParser(description='Program description')
[here come the rules...]
args = parser.parse_args()
do_something(args)
```
nuclear:
```python
from nuclear import CliBuilder

CliBuilder(help='Program description', run=do_something).has(
    [here come the rules...]
).run()
```

#### Migrating: Flags
argparse:
```python
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
```
nuclear:
```python
flag("-v", "--verbose", help="increase output verbosity"),
```

#### Migrating: Positional arguments
argparse:
```python
parser.add_argument("square", help="display a square of a given number", type=int)
```
nuclear:
```python
argument("square", help="display a square of a given number", type=int),
```

#### Migrating: Transferring values to functions
argparse:
```python
do_action(args.square, args.verbose)
```
nuclear:
```python
CliBuilder(run=do_action)  # invoking actions is done automatically by binding
```

## Installation
### Step 1. Prerequisites
- Python 3.6 (or newer)
- pip
#### on Debian 10 (buster)
```bash
sudo apt install python3.7 python3-pip
```
#### on Debian 9 (stretch)
Unfortunately, Debian stretch distribution does not have Python 3.6+ in its repositories, but it can be compiled from the source:
```bash
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xvf Python-3.6.9.tgz
cd Python-3.6.9
./configure --enable-optimizations --with-ensurepip=install
make -j8
sudo make altinstall
```
#### on Ubuntu 18
```bash
sudo apt install python3.6 python3-pip
```
#### on Centos 7
```bash
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
```
#### on Fedora
```bash
sudo dnf install python36
```

### Step 2. Install package using pip
Install package from [PyPI repository](https://pypi.org/project/nuclear) using pip:
```bash
pip3 install nuclear
```
Or using explicit python version:
```bash
python3.6 -m pip install nuclear
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
pip3 install -r requirements.txt -r requirements-dev.txt
./pytest.sh
```

## CliBuilder
`CliBuilder` is a main class of `nuclear` package which allows to build CLI definition.
It's a builder for Command Line Interface specification.
After that, you can invoke `.run()` method in order to parse provided arguments and invoke particular actions.

Empty CliBuilder has standard options enabled by default:

- `--help` - displaying usage and help
- `--version` - displaying application version number (if it has been defined)

### Step 1. Creating CliBuilder
In this step you can create new `CliBuilder` and set a custom configuration for it.
 The constructor is as follows:
```python
from nuclear import CliBuilder

CliBuilder(
           name: Optional[str] = None,
           version: Optional[str] = None,
           help: Optional[str] = None,
           run: Optional[Action] = None,
           with_defaults: bool = True,
           usage_onerror: bool = True,
           reraise_error: bool = False,
           hide_internal: bool = True,
)
```

`name` - name of the application for which the CLI is built

`version` - application version (displayed in help/version output)

`help` - short description of application

`run` - reference for a function which should be the default action for empty arguments list

`with_defaults` - whether default rules and actions should be added.
Defaults options are:
-h, --help: displaying help,
--version: displaying version,
--install-bash APP-NAME: installing application in bash with autocompleting,
--autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash

`usage_onerror` - wheter usage output should be displayed on syntax error

`reraise_error` - wheter syntax error should not be caught but reraised instead.
Enabling this causes stack trace to be flooded to the user.

`hide_internal` - wheter internal options (`--install-bash`, `--autocomplete`) should be hidden on help output.

### Step 2. Declaring CLI rules
The next step is to declare CLI rules for `CliBuilder` using `.has()` method

`has(*subrules: CliRule) -> 'CliBuilder'` method receives a CLI rules in its parameters and returns the `CliBuilder` itself for further building.
It is used to introduce the next level of sub-rules.

Available rules are:

- subcommand
- flag
- parameter
- argument
- arguments
- default_action
- primary_option

Example:
```python
from nuclear import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action

CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, usage_onerror=False, reraise_error=True).has(
    subcommand('checkout'),
    argument('commit'),
    arguments('files'),
    flag('-u', '--upstream', help='set upstream'),
    parameter('--count', type=int, required=True),
    default_action(lambda: print('default action')),
)
```

### Step 3. Running CLI arguments through parser
The final step is calling `.run()` on `CliBuilder`.
It parses all the CLI arguments passed to application.
Then it invokes triggered action which were defined before.
If actions need some parameters, they will be injected based on the parsed arguments.

Running empty builder:
```python
from nuclear import CliBuilder

CliBuilder().run()
```
just prints the standard help output, because it's the default action for an empty builder if no arguments are provided.

## Sub-commands
Commands may form a multilevel tree with nested sub-commands.
Sub-commands syntax is commonly known, e.g.:

- `git remote rename ...`
- `docker container ls`
- `nmcli device wifi list`
- `ip address show`

Sub-commands split the CLI into many nested CLI levels, forming a tree.
They decide where to direct the parser, which seeks for a most relevant action to invoke and decides which rules are active.

Sub-commands create nested levels of sub-parsers, which not only may have different actions but also contains different CLI rules, such as named parameters, flags or other sub-commands, which are only enabled when parent command is enabled as well.
Subcommand can have more subrules which are activated only when corresponding subcommand is active.
So subcommand is just a keyword which narrows down the context.

### Sub-commands specification
In order to create subcommand rule specification, use:
```python
from nuclear import subcommand

subcommand(
        *keywords: str,
        run: Optional[Action] = None,
        help: str = None,
)
```

`keywords` - possible keyword arguments which any of them triggers a subcommand

`run` - optional action to be invoked when subcommand is matched

`help` - description of the parameter displayed in help output

### Nesting sub-commands
With sub-commands, you can nest other CLI rules.
They will be active only when corresponding subcommand is active.

Subrules can be nested using `.has(*subrules: CliRule)` method.
It returns itself for further building, so it can be used just like `CliBuilder`:
```python
from nuclear import CliBuilder, argument, subcommand

CliBuilder().has(
    subcommand('nmcli').has(
        subcommand('device').has(
            subcommand('wifi').has(
                subcommand('list'),
            ),
        ),
    ),
    subcommand('ip').has(
        subcommand('address', 'a').has(
            subcommand('show'),
            subcommand('del').has(
                argument('interface'),
            ),
        ),
    ),
)
```
In that manner, the formatted code above is composing a visual tree, which is clear.

### Sub-commands example: subcommands.py
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, subcommand

CliBuilder('subcommands-demo', run=lambda: print('default action')).has(
    subcommand('remote', run=lambda: print('action remote')).has(
        subcommand('push', run=lambda: print('action remote push')),
        subcommand('rename', run=lambda: print('action remote rename')),
    ),
    subcommand('checkout', run=lambda: print('action checkout')),
    subcommand('branch', run=lambda: print('action branch')),
).run()
```
Usage is quite self-describing:
```console
foo@bar:~$ ./subcommands.py remote
action remote
foo@bar:~$ ./subcommands.py remote push
action remote push
foo@bar:~$ ./subcommands.py branch
action branch
foo@bar:~$ ./subcommands.py
default action
foo@bar:~$ ./subcommands.py --help
subcommands-demo

Usage:
  ./subcommands.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

Commands:
  remote        - List remotes
  remote push  
  remote rename
  checkout      - Switch branches
  branch        - List branches

Run "./subcommands.py COMMAND --help" for more information on a command.
```

See [sub-commands tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_subcommand.py) for more detailed use cases.

## Flags
Flag is a boolean parameter which is toggled by single keyword.
There are supported both short (`-f`) and long (`--force`) formats.

In order to create flag rule specification, use:
```python
from nuclear import flag

flag(
        *keywords: str,
        help: str = None,
        multiple: bool = False,
)
```
`keywords` are arguments (one or many) which any of them enables flag when it occurs.
Flag value is `False` by default.
Flag keywords may be passed using direct format: `-f` or `--flag`,
as well as by name: `f` or `flag`, which will be also evaluated to `-f` or `--flag`.
Single character flags will get single hyphen prefix (`-f`),
longer flag names will get double hyphen prefix (`--flag`).

`help` is description of the flag displayed in help output

`multiple` - whether flag is allowed to occur many times.
Then flag has int type and stores number of its occurrences

Example:
```python
from nuclear import CliBuilder, flag

CliBuilder(run=lambda force: print(force)).has(
    flag('--force', '-f'),
).run()
```
Usage:
```console
foo@bar:~$ ./example.py --force
True
foo@bar:~$ ./example.py
False
``` 

### Combining short flags
Many short flags may be combined in one argument. Instead of `-t -u -l -p -n` you can just type `-tulpn`.

### Multiple flag occurrences
Multiple occurences are also supported for flags. When `multiple` is set to `True`, then the flag value represents how many times it was set. The value type is then `int`, not `bool`.
```python
CliBuilder(run=lambda verbose: print(f'verbosity level: {verbose}')).has(
    flag('verbose', 'v', multiple=True),
).run()
```
Then `-vvv` should return `3`.

See [flag tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_flag.py) for more detailed use cases.
## Named parameters
Parameter is a named value, which will be injected to triggered action by its name.
There are supported both manners for setting parameter value:
`--parameter-name value` or `--parameter-name=value`

Named parameters may appear anywhere in CLI arguments list: at the beginning or at the end, or even before positional arguments.
As long as they are matched as named parameters, they will not be recognized as positional arguments.

The parameters may be later referenced by its name or keywords
(in lowercase format without hyphen prefix and with underscores instead of dashes,
e.g. `--paramater-name` will be injected as `parameter_name`)

In order to create parameter rule specification, use:
```python
from nuclear import parameter

parameter(
        *keywords: str,
        name: str = None,
        help: str = None,
        required: bool = False,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
        strict_choices: bool = False,
        multiple: bool = False,
)
```
`keywords` keyword arguments which are matched to parameter.
Parameter keywords may be passed using direct format: `-p` or `--param`,
as well as by name: `p` or `param`, which will be evaluated to `-p` or `--param`.
Single character parameter will get single hyphen prefix (`-p`),
longer parameter names will get double hyphen prefix (`--param`)

`name` is explicit paramter name (can be used, when it's different from any keyword)

`help` is description of the parameter displayed in help output

`required` tells whether parameter is required.
If it's required but it's not given, the syntax error will be raised.

`default` is default value for the parameter, if it's not given (and it's not required).

`type` is a type of parameter value (e.g. str, int, float).
Reference to a parser function may be provided here as well.
Then parameter value is evaluated by passing the string argument value to that function.

`choices` is Explicit list of available choices for the parameter value
or reference to a function which will be invoked to retrieve such possible values list

`strict_choices` - whether given arguments should be validated against available choices

`multiple` - whether parameter is allowed to occur many times.
Then parameter has list type and stores list of values

Basic parameter example:
```python
from nuclear import CliBuilder, parameter

CliBuilder(run=lambda param: print(param)).has(
    parameter('param', 'p'),
).run()
```
```console
foo@bar:~$ ./example.py --param OK
OK
foo@bar:~$ ./example.py --param=OK
OK
foo@bar:~$ ./example.py -p OK
OK
foo@bar:~$ ./example.py
None
```

### Multiple parameter occurrences
Multiple occurences are also supported for parameters.
When `multiple` is set to `True`, then the parameter value represents list of values and can be appended mutliple times.
The value type is then `list`.
```python
def what_to_skip(skip: List[str]):
    print(f'skipping: {skip}')

CliBuilder(run=what_to_skip).has(
    parameter('skip', multiple=True, type=str),
).run()
```
```console
foo@bar:~$ ./example.py --skip build --skip run
skipping: ['build', 'run']
``` 

See [parameter tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_param.py) for more detailed use cases.

## Positional arguments
Positional argument is an unnamed parameter, which is recognized only by its position on their order in command line arguments list.
For example first two arguments (except flags and named parameters) may be detected as positional arguments and matched to corresponding variables.

### Single positional arguments
Let's assume we have CLI syntax: `git push <origin> <master>`.
`git` is application binary name of course, `push` is a sub-command, which have 2 positional arguments: `origin` and `master`.

In order to create positional argument rule specification, use:
```python
from nuclear import argument

def argument(
        name: str,
        help: str = None,
        required: bool = True,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
        strict_choices: bool = False,
)
```

`name` - internal argument name, which will be used to reference argument value

`help` - description of the argument displayed in help output

`required` - whether positional argument is required.
If it's required but it's not given, the syntax error will be raised.

`default` - default value for the argument, if it's not given (and it's not required)

`type` - type of argument value (e.g. str, int, float)
Reference to a parser function may be provided here as well.
Then argument value is evaluated by passing the string argument value to that function.

`choices` - Explicit list of available choices for the argument value
or reference to a function which will be invoked to retrieve such possible values list.

`strict_choices` - whether given arguments should be validated against available choices

#### Example: pos-args.py
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument


def print_args(remote: str, branch: str):
    print(f'remote: {remote}, argument: {branch}')


CliBuilder('pos-args', run=print_args).has(
    argument('remote', help='remote name', type=str, choices=['origin', 'local']),
    argument('branch', help='branch name', required=False, default='master'),
).run()
```
Usage:
```console
foo@bar:~$ ./pos-args.py --help
pos-args

Usage:
  ./pos-args.py [OPTIONS] REMOTE [BRANCH]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

foo@bar:~$ ./pos-args.py
[ERROR] Syntax error: required positional argument "remote" is not given
pos-args

Usage:
  ./pos-args.py [OPTIONS] REMOTE [BRANCH]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

foo@bar:~$ ./pos-args.py origin
remote: origin, argument: master

foo@bar:~$ ./pos-args.py origin develop
remote: origin, argument: develop
```

See [positional arguments tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_positional_argument.py) as a specification.
## Many positional arguments
`nuclear` allows to match all remaining (not already matched) arguments.
It can be useful when using syntax like `docker cmd`:
```docker run cmd ubuntu /bin/bash -c /script.sh```
With that syntax all arguments after `ubuntu` - `/bin/bash -c /script.sh` should be matched to one variable. 

You can do it with `nuclear` using `arguments`.
That rule will force parser to store all remaining arguments in a list variable (or in a joined string).

In order to create "multiple arguments" rule specification, use:
```python
from nuclear import arguments

def arguments(
        name: str,
        type: Union[Type, Callable[[str], Any]] = str,
        choices: Union[List[Any], Callable[..., List[Any]]] = None,
        strict_choices: bool = False,
        count: Optional[int] = None,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
        joined_with: Optional[str] = None,
        help: str = None,
)
```
It allows to retrieve specific number of CLI argumetns or all remaining arguments.
All matched arguments will be extracted to a list of arguments or a string (depending on `joined_with` parameter)

`name` - internal variable name, which will be used to reference matched arguments

`type` - explicit type of arguments values (e.g. str, int, float)
Reference to a parser function may be provided here as well.
Then argument value is evaluated by passing the string argument value to that function

`choices` - Explicit list of available choices for the argument value
or reference to a function which will be invoked to retrieve such possible values list.

`strict_choices` - whether given arguments should be validated against available choices

`count` - explicit number of arguments to retrieve.
If undefined, there is no validation for arguments count.
If you need particular number of arguments, you can use this count instead of setting min_count=max_count.

`min_count` - minimum number of arguments.
By default, there is no lower limit (it is 0).

`max_count` - maximum number of arguments.
If undefined, there is no upper limit for arguments count.

`joined_with` - optional string joiner for arguments.
If it's set, all matched arguments will be joined to string with that joiner.
It it's not given, matched arguments will be passed as list of strings.
This value (string or list) can be accessed by specified name, when it's being injected to a function.

`help` - description of the arguments displayed in help output

Note that `arguments(count=1)` rule with is like single `argument` rule, except that it stores list with one element.

You can use many consecutive `arguments` rules as long as they have `count` or `max_count` set.

### Example: many-args.py
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, arguments, subcommand


def run_cmd(cmd: str):
    print(f'cmd: {cmd}')


CliBuilder('many-args').has(
    subcommand('run', run=run_cmd).has(
        arguments('cmd', joined_with=' '),
    ),
).run()
```
Usage:
```console
foo@bar:~$ ./many-args.py
many-args

Usage:
  ./many-args.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

Commands:
  run [CMD...]

Run "./many-args.py COMMAND --help" for more information on a command.

foo@bar:~$ ./many-args.py run /bin/bash -c script.sh
cmd: /bin/bash -c script.sh

foo@bar:~$ ./many-args.py run "/bin/bash -c script.sh"
cmd: /bin/bash -c script.sh
```

See [many arguments tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_many_arguments.py) for more detailed use cases.

## Dictionaries
Dictionary contains key-value pairs.
You can add multiple values to it by passing arguments in a manner:
`-c name1 value1 -c name2 value2`.

By default it stores empty Python dict.
These values may be later referenced as dict by its explicit name or keywords
(in lowercase format without hyphen prefix and with underscores instead of dashes,
e.g. `--config-name` will be injected as `config_name` variable name)

In order to create dictionary rule specification, use:
```python
from nuclear import dictionary

dictionary(
        *keywords: str,
        name: str = None,
        help: str = None,
        key_type: Union[Type, Callable[[str], Any]] = str,
        value_type: Union[Type, Callable[[str], Any]] = str,
)
```

`keywords` - keyword arguments which are matched to this dictionary.
Keywords may be passed using direct format: `-c` or `--config`,
as well as by name: `c` or `config`, which will be evaluated to `-c` or `--config`.
Single character dictionary will get single hyphen prefix (`-c`),
longer dictionary names will get double hyphen prefix (`--config`)

`name` - explicit internal dictionary name (can be used to distinguish it from any keyword)

`help` - description of the dictionary displayed in help output

`key_type` - type of dictionary key (e.g. str, int, float)
Reference to a parser function may be provided here as well.
Then dictionary value is evaluated by passing the string argument value to that function.

`value_type` - type of dictionary value (e.g. str, int, float)
Reference to a parser function may be provided here as well.
Then dictionary value is evaluated by passing the string argument value to that function.

Basic dictionary example:
```python
from nuclear import CliBuilder, dictionary

CliBuilder(run=lambda config: print(config)).has(
    dictionary('config', 'c', value_type=int),
).run()
```
```console
foo@bar:~$ ./example.py --config key1 5 -c key2 42
{'key1': 5, 'key2': 42}
foo@bar:~$ ./example.py
{}
```

See [dictionaries tests](https://github.com/igrek51/nuclear/blob/master/tests/parser/test_dictionary.py) for more detailed use cases.

## Auto-completion
Shell autocompletion allows to suggest most relevant hints on hitting `Tab` key, while typing a command line.

Auto-completion provided by `nuclear` is enabled by default to all known keywords based on the declared subcommands and options.

Defining possible choices may imporove auto-completing arguments. You can declare explicit possible values list or a function which provides such a list at runtime.

**completers.py**:
```python
#!/usr/bin/env python3
import re
from typing import List

from nuclear import CliBuilder, parameter, default_action
from nuclear.utils.shell import shell, shell_output


def list_screens() -> List[str]:
    """Return list of available screen names in a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def adjust_screen(output: str, mode: str):
    shell(f'xrandr --output {output} --mode {mode}')


CliBuilder('completers-demo').has(
    parameter('output', choices=list_screens, required=True),
    parameter('mode', choices=['640x480', '800x480', '800x600'], required=True),
    default_action(adjust_screen),
).run()
```

In order to enable auto-completion, you need to install some extension to bash. Fortunately `nuclear` has built-in tools to do that:
```console
foo@bar:~$ sudo ./completers.py --install-bash completers-demo
[info]  creating link: /usr/bin/completers-demo -> ~/nuclear/docs/example/completers.py
#!/bin/bash
_autocomplete_98246661() {
COMPREPLY=( $(completers-demo --autocomplete "${COMP_LINE}") )
}
complete -F _autocomplete_98246661 completers-demo
[info]  Autocompleter has been installed in /etc/bash_completion.d/autocomplete_completers-demo.sh. Please restart your shell.
```
Now, we have `completers-demo` application installed in `/usr/bin/` (symbolic link to the current script) and bash completion script installed as well.
We can hit `[Tab]` key to complete command when typing. Here are some completions examples:
```console
foo@bar:~$ completers-d[Tab]
foo@bar:~$ completers-demo

foo@bar:~$ completers-demo [Tab][Tab]
--autocomplete  -h                   --mode               --output
--install-bash       --help               --mode=              --output=

foo@bar:~$ completers-demo --mo[Tab]
foo@bar:~$ completers-demo --mode

foo@bar:~$ completers-demo --mode [Tab][Tab]
640x480  800x480  800x600

foo@bar:~$ completers-demo --mode 640[Tab]
foo@bar:~$ completers-demo --mode 640x480

foo@bar:~$ completers-demo --mode 640x480 --output [Tab][Tab]
eDP-1   HDMI-1
```

### Custom completers
You can provide your custom auto-completers (providers of possible values) to the `choices` parameter.

The example is the function which returns a list of available screens:
```python
def list_screens() -> List[str]:
    """Return list of available screen names in a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]
```
You can use it to validate and propose available choices for parameter or positional argument:
```python
CliBuilder().has(
    parameter('output', choices=list_screens, required=True),
)
```

### Installing Autocompletion
In order to enable the autocompletion, there must be a specific script in `/etc/bash_completion.d/`.
With `nuclear` you just need to run:
```console
# sudo ./sample-app.py --install-bash sample-app
```
It will install autocompletion script and add a symbolic link in `/usr/bin/`,
so as you can run your app with `sample-app` command instead of `./sample_app.py`.

Now you can type `sample-app` and hit `Tab` to see what are the possible commands and options.

If you type `sample-app --he`, it will automatically fill the only possible option: `--help`.

Sometimes, you need to make some modifications in your code,
but after these modifications you will NOT need to reinstall autocompletion again.
You had to do it only once, because autocompletion script only redirects its query and run `sample_app.py`:
```console
sample-app --autocomplete "sample-app --he"
```

### How does auto-completion work?
1. While typing a command in `bash`, you hit `Tab` key. (`your-app.py cmd[TAB]`)
2. `bash` looks for an autocompletion script in `/etc/bash_completion.d/`.
There should be a script installed for your command after running `--install-bash` on your application.
So when it's found, this script is called by bash.
3. The autocompletion script redirects to your application, running it with `--autocomplete` option, namely script runs `your-app.py --autocomplete "cmd"`, asking it for returning the most relevant command proposals.
Notice that in that manner, the autocompletion algorithm is being run always in up-to-date version.
4. `your-app.py` has `--autocomplete` option enabled by default so it starts to analyze which keyword from your CLI definition is the most relevant to the currently typed word (`cmd`).
5. If you defined custom completers functions, they will be invoked right now (if needed) in order to get up-to-date proposals and analyze them as well. 
6. `your-app.py` returns a list of proposals to the `bash`.
7. `bash` shows you these results.
If there's only one matching proposal, the currently typed word is automatically filled.

Note that your application is being run each time when trying to get matching arguments proposals.

## Auto-generated help
`nuclear` auto-generates help and usage output based on the defined CLI rules.

Let's say we have quite complex CLI definition:
```python
CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, usage_onerror=False, reraise_error=True).has(
    subcommand('git').has(
        subcommand('push', run=git_push).has(
            argument('remote'),
            argument('branch', required=False),
            flag('-u', '--upstream', help='set upstream'),
        ),
        subcommand('help', help='show help', run=lambda: print('show help')),
        subcommand('checkout', 'co', help='checkout branch').has(
            argument('branch', choices=['master', 'feature', 'develop'], type=str),
            flag('force', 'f'),
        ),
        subcommand('remote', help='show remotes list').has(
            subcommand('set-url', 'rename', help="change remote's name").has(
                argument('remote-name', choices=['origin', 'backup'], type=str),
                argument('new-name'),
            ),
        ),
        parameter('--date', type=iso_datetime),
        parameter('--count', type=int, required=True),
        parameter('--work-tree', type=existing_directory, default='.', help='working directory'),
    ),
    subcommand('xrandr').has(
        parameter('output', required=True, choices=list_screens),
        flag('primary', 'p'),
        default_action(xrandr_run)
    ),
    subcommand('docker').has(
        subcommand('exec', run=docker_exec).has(
            parameter('-u', name='user', type=int),
            argument('container-name'),
            arguments(name='cmd', joined_with=' '),
        ),
    ),
    default_action(lambda: print('default action')),
)
```

We can see the usage and description of commands using `--help` or `-h`:
```console
foo@bar:~$ python3 multiapp.py --help
multiapp v1.0.0 - many apps launcher

Usage:
  multiapp.py [COMMAND] [OPTIONS]

Options:
  --version                        - Print version information and exit
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --install-bash APP-NAME          - Install script as a bash binary and add autocompletion links
  --autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  git                                           
  git push REMOTE [BRANCH]                      
  git help                                       - show help
  git co|checkout BRANCH                         - checkout branch
  git remote                                     - show remotes list
  git remote rename|set-url REMOTE-NAME NEW-NAME - change remote's name
  xrandr                                        
  docker                                        
  docker exec CONTAINER-NAME [CMD...]           

Run "multiapp.py COMMAND --help" for more information on a command.
```

### Sub-commands help
We can also check the usage for a selected sub-command only:
```console
foo@bar:~$ python3 multiapp.py git --help
multiapp v1.0.0 - many apps launcher

Usage:
  multiapp.py git [COMMAND] [OPTIONS]

Options:
  --date DATE                     
  --count COUNT                   
  --work-tree WORK_TREE            - working directory
  --version                        - Print version information and exit
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

Commands:
  push REMOTE [BRANCH]                      
  help                                       - show help
  co|checkout BRANCH                         - checkout branch
  remote                                     - show remotes list
  remote rename|set-url REMOTE-NAME NEW-NAME - change remote's name

Run "multiapp.py git COMMAND --help" for more information on a command.
```

### version check
Use `--version` in order to show your application version:
```console
foo@bar:~$ python3 multiapp.py --version
multiapp v1.0.0 (nuclear v1.0.1)
```

## Data types
`nuclear` supports typed values for parameters or positional arguments.
By default, all values have string types.
It can be changed by defining `type` parameter.

There are 2 possible `type` values:
- type name itself (e.g. `int`, `str`, `float`)
- reference for a parser which returns a value
In both cases, the internal variable value is calculated by invoking `type(str_value)`.
When argument value has invalid format, there is syntax error raised. 

### Basic types (int, float, etc.)
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

def print_it(count: int):
    print(count * 2)

CliBuilder(run=print_it).has(
    argument('count', type=int),
).run()
```
```console
foo@bar:~$ ./example.py 21
42

foo@bar:~$ ./example.py dupa
[ERROR] Syntax error: parsing positional argument "count": invalid literal for int() with base 10: 'dupa'
Usage:
  ./pyt.py [OPTIONS] COUNT

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

foo@bar:~$ ./example.py
[ERROR] Syntax error: required positional argument "count" is not given
Usage:
  ./pyt.py [OPTIONS] COUNT

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
```

### Built-in data types
`nuclear` has built-in parsers / validators for some types

#### Filesystem types
- `nuclear.types.filesystem.existing_file` validates if given string is an existing regular file (not a directory).
After validation, the value is internally stored as `str`.
```python
from nuclear.types.filesystem import existing_file

argument('file', type=existing_file)
```

- `nuclear.types.filesystem.existing_directory` validates if given string is an existing directory.
After validation, the value is internally stored as `str`.
```python
from nuclear.types.filesystem import existing_directory

argument('file', type=existing_directory)
```

#### Datetime types
- `nuclear.types.time.iso_date` parses / validates given string as a date in ISO format: `%Y-%m-%d`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.types.time import iso_date

argument('date', type=iso_date)
```

- `nuclear.types.time.iso_time` parses / validates given string as a time in ISO format: `%H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.types.time import iso_time

argument('time', type=iso_time)
```

- `nuclear.types.time.iso_time` parses / validates given string as a datetime in ISO format: `%Y-%m-%d %H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.types.time import iso_datetime

argument('datetime', type=iso_datetime)
```
Example:
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.types.time import iso_datetime
from datetime import datetime

def print_it(to: datetime):
    print(to)

CliBuilder(run=print_it).has(
    argument('to', type=iso_datetime),
).run()
```
```console
foo@bar:~$ ./example.py 2019-07-13
[ERROR] Syntax error: invalid datetime format: 2019-07-13
Usage:
  ./pyt.py [OPTIONS] TO

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

foo@bar:~$ ./example.py "2019-07-13 20:00:05"
2019-07-13 20:00:05
```

- `nuclear.types.time.datetime_format` parses / validates given string as a datetime in custom formats specified by user.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.types.time import datetime_format
from datetime import datetime

def print_it(to: datetime):
    print(to)

CliBuilder(run=print_it).has(
    argument('to', type=datetime_format('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d')),
).run()
```
```console
foo@bar:~$ ./example.py "2019-07-13 20:00:05"
2019-07-13 20:00:05
foo@bar:~$ ./example.py 2019-07-13
2019-07-13 00:00:00
```

- `nuclear.types.time.today_format` parses / validates given string as a time in custom formats specified by user.
It gets time from input and combines it with the today date.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.types.time import today_format
from datetime import datetime

def print_it(to: datetime):
    print(to)

CliBuilder(run=print_it).has(
    argument('to', type=today_format('%H:%M:%S', '%H:%M')),
).run()
```
```console
foo@bar:~$ ./example.py 12:42
2019-07-13 12:15:00
```

### Custom type parsers
You can define custom parser/validator function.
It should take one `str` argument and return expected value type.

```python
#!/usr/bin/env python3
import re
from dataclasses import dataclass
from nuclear import CliBuilder, argument

@dataclass
class Person:
    name: str
    age: int

    @staticmethod
    def parse(arg: str) -> 'Person':
        match = re.compile('(.+)-([0-9]+)').match(arg)
        return Person(match.group(1), int(match.group(2)))
        

def print_it(human: Person):
    print(human)

CliBuilder(run=print_it).has(
    argument('human', type=Person.parse),
).run()
```
```console
foo@bar:~$ ./example.py Eric-33
Person(name='Eric', age=33)
```

## Errors handling
`nuclear` validates passed CLI arguments on running `CliBuilder.run()`

### Handling syntax errors - CliSyntaxError
In case of syntax error, `CliBuilder.run()` raises `CliSyntaxError`, it's when:

- parameter value is missing: `--param-name` without next argument
- required parameter is not given
- required positional argument is not given
- positiona argument or parameter has invalid type (there was parsing type error)

By default `CliSyntaxError` caught by `CliBuilder` is rethrown.
You can disable raising this error again by seting `reraise_error = False` when creating `CliBuilder`:
`CliBuilder(reraise_error = False)`.
Then only the error log will be displayed in console stdout.

`usage_onerror` parameter decides wheter usage output should be displayed on syntax error.

#### Erros handling example
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

CliBuilder(usage_onerror=False).has(
    argument('remote', required=True),
).run()
```

```console
foo@bar:~$ ./pos-args.py
[ERROR] Syntax error: required positional argument "remote" is not given
```

### CliDefinitionError
In case of invalid CLI definition, `CliBuilder.run()` raises `CliDefinitionError`. It's e.g. when:

- positional argument or parameter is set to required and has default value set (it doesn't make any sense)
- positional argument is placed after all remaining arguments
- parameter / argument value does not belong to strict available choices list

#### Wrong CLI Definition example
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

CliBuilder().has(
    argument('remote', required=True, default='def'),
).run()
```

```console
foo@bar:~$ ./errors.py
[ERROR] CLI Definition error: argument value may be either required or have the default value
Traceback (most recent call last):
  File "pyt.py", line 4, in <module>
    argument('remote', required=True, default='def'),
  File "~/nuclear/nuclear/builder/builder.py", line 69, in run
    self.run_with_args(sys.argv[1:])
  File "~/nuclear/nuclear/builder/builder.py", line 76, in run_with_args
    raise e
  File "~/nuclear/nuclear/builder/builder.py", line 73, in run_with_args
    Parser(self.__subrules).parse_args(args)
  File "~/nuclear/nuclear/parser/parser.py", line 37, in __init__
    self._init_rules()
  File "~/nuclear/nuclear/parser/parser.py", line 57, in _init_rules
    raise CliDefinitionError('argument value may be either required or have the default value')
nuclear.parser.error.CliDefinitionError: argument value may be either required or have the default value
```

## CLI Rules cheatsheet
Here is the cheatsheet for the most important CLI rules:
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

## Complex CLI tree
Here's an example of more complex CLI definition tree:

**multiapp.py**:
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action
from nuclear.types.filesystem import existing_directory
from nuclear.types.time import iso_datetime


def main():
    CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
               with_defaults=True, usage_onerror=False, reraise_error=True, hide_internal=True).has(
        subcommand('git').has(
            subcommand('push', run=git_push).has(
                argument('remote'),
                argument('branch', required=False),
                flag('-u', '--upstream', help='set upstream'),
            ),
            subcommand('help', help='show help', run=lambda: print('show help')),
            subcommand('checkout', 'co', help='checkout branch').has(
                argument('branch', choices=['master', 'feature', 'develop'], type=str),
                flag('force', 'f'),
            ),
            subcommand('remote', help='show remotes list').has(
                subcommand('set-url', 'rename', help="change remote's name").has(
                    argument('remote-name', choices=['origin', 'backup'], type=str),
                    argument('new-name'),
                ),
            ),
            parameter('--date', type=iso_datetime),
            parameter('--count', type=int, required=True),
            parameter('--work-tree', type=existing_directory, default='.', help='working directory'),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=list_screens),
            flag('primary', 'p'),
            default_action(xrandr_run)
        ),
        subcommand('docker').has(
            subcommand('exec', run=docker_exec).has(
                parameter('-u', name='user', type=int),
                argument('container-name'),
                arguments(name='cmd', joined_with=' '),
            ),
        ),
        default_action(lambda: print('default action')),
    ).run()


def git_push(remote: str, branch: str, upstream: bool):
    print(f'git push: {remote}, {branch}, {upstream}')


def xrandr_run(output, primary):
    print(f'xrandr: {output} {primary}')


def list_screens():
    return ['eDP1', 'HDMI2']


def docker_exec(user: int, container_name: str, cmd: str):
    print(f'docker exec {user}, {container_name}, {cmd}')


if __name__ == '__main__':
    main()
```

Usage:
```console
foo@bar:~$ ./multiapp.py --help
multiapp v1.0.0 - many apps launcher

Usage:
  ./multiapp.py [COMMAND] [OPTIONS]

Options:
  --version                        - Print version information and exit
  -h, --help [SUCOMMANDS...]       - Display this help and exit
  --install-bash APP-NAME          - Install script as a bash binary and add autocompletion links
  --autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  git                                           
  git push REMOTE [BRANCH]                      
  git help                                       - show help
  git co|checkout BRANCH                         - checkout branch
  git remote                                     - show remotes list
  git remote rename|set-url REMOTE-NAME NEW-NAME - change remote's name
  xrandr                                        
  docker                                        
  docker exec CONTAINER-NAME [CMD...]           

Run "./multiapp.py COMMAND --help" for more information on a command.
```

