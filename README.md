# cliglue - glue for CLI
[![Build Status](https://travis-ci.org/igrek51/cliglue.svg?branch=master)](https://travis-ci.org/igrek51/cliglue)
[![PyPI version](https://badge.fury.io/py/cliglue.png)](https://badge.fury.io/py/cliglue)

`cliglue` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.

`cliglue` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the "glue" code for binding & parsing parameters every time.
So it makes writing console aplications faster and simpler.

## Features
- [Auto-generated help and usage](doc/help.md) (`--help`)
- [Shell autocompletion](doc/autocompletion.md) (getting most relevant hints on hitting `Tab`)
- [Multilevel sub-commands](doc/subcommands.md) (e.g. `git remote add ...` syntax)
- [Named parameters](doc/parameters.md): supporting both `--name value` and `--name=value`
- [Flags](doc/flags.md): supporting both short (`-f`) and long (`--force`)
- [Positional arguments](doc/positional-args.md) (e.g. `git push <origin> <master>`)
- Invoking matched action function & providing corresponding parameters
- [Custom type validators / parsers](doc/data-types.md)
- [Custom auto-completers](doc/autocompletion.md) (providers of possible values)
- [Parameters validation, handling syntax errors](doc/errors.md)
- [Typed values](doc/data-types.md) (int, time, date, file, etc.)
- Default values for optional arguments
- [Standard options](doc/builder.md) enabled by default (`--help`, `--version`)
- [Declarative CLI builder](doc/complex-usage.md)

## Quick start
Let's create simple command-line application using `cliglue`.
Let's assume we have a function as follows:
```python
def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)
```
and we need a glue which binds it with a CLI (Command-Line Interface).
We want it to be run with different parameters provided by user to the terminal shell in a manner:
`./hello.py WORLD --reverse --repeat=1`.
We've identified one positional argument, a flag and a numerical parameter.
So our CLI definition may be declared using `cliglue`:
```python
CliBuilder('hello-app', run=say_hello).has(
    argument('name'),
    flag('reverse'),
    parameter('repeat', type=int, default=1),
)
```
Getting all together, we've binded our function with a CLI definition:

**hello.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, flag, parameter


def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)


def main():
    CliBuilder('hello-app', run=say_hello).has(
        argument('name'),
        flag('reverse'),
        parameter('repeat', type=int, default=1),
    ).run()


if __name__ == '__main__':
    main()
```

Let's trace what is happening here:
- `CliBuilder` is used to build CLI tree for entire application.
- `'hello-app'` is a name for that application to be displayed in help output.
- `run=say_hello` sets default action for the application. Now a function `say_hello` is binded as a main action and will be invoked if no other action is matched.
- `.has(...)` allows to embed other rules inside that builder.
- `argument('name')` declares positional argument. From now, first CLI argument (after binary name) will be recognized as `name` variable.
- `flag('reverse')` binds `--reverse` keyword to a flag named `reverse`. So as it may be used later on.
- `parameter('repeat', type=int, default=1)` binds `--repeat` keyword to a parameter named `repeat`, which type is `int` and its default value is `1`.
- Finally, invoking `.run()` does all the magic.
It gets system arguments list, starts to process them and invokes relevant action.

### Help / Usage
`CliBuilder` has some basic options added by default, like `--help` or `--version`.
Thus, you can check the usage by running application with `--help` flag:
```console
foo@bar:~$ ./hello.py --help
hello-app

Usage:
  ./hello.py [OPTIONS] NAME

Options:
  -h, --help [SUCOMMANDS...]       - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals
  --reverse                       
  --repeat REPEAT                 
```

Notice there are already rules being displayed, which were declared before:
- positional argument `name`: `./hello.py [OPTIONS] NAME`
- flag `reverse`: `--reverse`
- parameter `repeat`: `--repeat REPEAT`

### Injecting parameters
Now when we execute our application with one argument provided, we get:
```console
foo@bar:~$ ./hello.py world
Hello world.
```
Note that `world` was matched to `name` argument.
We've binded `say_hello` as a default action, so it has been invoked with particular parameters:
```python
say_hello(name='world', reverse=False, repeat=1)
```
- positional argument `name` has been assigned a `'world'` value.
- flag `reverse` was not given, so it's `False` by default.
- parameter `repeat` was not given either, so it was set to its default value `1`.

Let's provide all of the parameters explicitly, then we get:
```console
foo@bar:~$ ./hello.py --reverse world --repeat 2
Hello dlrow.Hello dlrow.
```
Or we can do the same in a different way:
```console
foo@bar:~$ ./hello.py world --repeat=2 --reverse
Hello dlrow.Hello dlrow.
```

## How does it work?
1. You define all required CLI rules for your program in a declarative tree.
2. User provides command-line arguments when running program in a shell.
3. `cliglue` parses and validates all the parameters, flags, sub-commands, positional arguments, etc.
4. `cliglue` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `cliglue` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `cliglue` will handle all the rest for you.

## `cliglue` vs `argparse`
Why to use `cliglue`, since we already have Python `argparse`? Here are some subjective advantages of `cliglue`:
- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building,
- CLI definition code as a clear documentation.

### Migrating from `argparse` to `cliglue`
TODO

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
#### on Ubuntu
```bash
sudo apt install python3.6 python3-pip
```
#### on Centos
```bash
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
```

### Step 2. Install package using pip
Install package from [PyPI repository](https://pypi.org/project/cliglue) using pip:
```bash
pip3 install cliglue
```
Or using explicit python version:
```bash
python3.6 -m pip install cliglue
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

