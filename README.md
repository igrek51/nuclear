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
and we need a glue which binds it with a CLI.
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
4. `cliglue` finds the most relevant action and invokes it.
5. When invoking a function, `cliglue` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `cliglue` will handle all the rest for you.

## `cliglue` vs `argparse`
Why `cliglue`, since we already have Python `argparse`? Here are some subjective advantages of `cliglue`:
- declarative way of CLI logic in one place
- autocompletion out of the box
- easier way of building multilevel sub-commands
- automatic action binding & injecting arguments, no need to pass `args` to functions manually
- simpler & concise CLI building
- CLI definition code as a clear documentation

## Installation
### Prerequisites
Install Python 3.6 (or newer) with pip
#### on Ubuntu
```console
sudo apt install python3.6 python3-pip
```
#### on Centos
```console
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
```
#### on Debian 9 (stretch)
Unfortunately, current official Debian distribution does not have Python 3.6 in its repositories, but it can be compiled from the source:
```console
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xvf Python-3.6.9.tgz
cd Python-3.6.3
./configure --enable-optimizations --with-ensurepip=install
make -j8
sudo make altinstall
```
### Install package using pip
Install package from [PyPI repository](https://pypi.org/project/cliglue) using pip:
```console
sudo pip3 install cliglue
```
Or using explicit python version:
```console
python3.6 -m pip install cliglue
```
### Install package in develop mode
Clone repo and install dependencies:
```bash
pip3 install -r requirements.txt
```
Then install package in develop mode in order to make any changes for your own:
```bash
python3 setup.py develop
```

## Testing
Running tests:
```bash
pip3 install -r requirements.txt -r requirements-test.txt
./pytest.sh
```


## More examples

### Sub-commands
Commands may build a multilevel tree with nested sub-commands (similar to `git`, `nmcli` or `ip` syntax).

**subcommands.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, subcommand


def main():
    CliBuilder('subcommands-demo', run=lambda: print('default action')).has(
        subcommand('remote', run=lambda: print('action remote')).has(
            subcommand('push', run=lambda: print('action remote push')),
            subcommand('rename', run=lambda: print('action remote rename')),
        ),
        subcommand('checkout', run=lambda: print('action checkout')),
        subcommand('branch', run=lambda: print('action branch')),
    ).run()


if __name__ == '__main__':
    main()
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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  remote        - List remotes
  remote push  
  remote rename
  checkout      - Switch branches
  branch        - List branches

Run "./subcommands.py COMMAND --help" for more information on a command.
```

### Auto-completion
Defining choices may help in auto-completing arguments. You can declare explicit possible values list or a function which provides such a list at runtime.

**completers.py**:
```python
#!/usr/bin/env python3
import re
from typing import List

from cliglue import CliBuilder, parameter, default_action
from cliglue.utils.shell import shell, shell_output


def list_screens() -> List[str]:
    """Return list of available screen names in a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def adjust_screen(output: str, mode: str):
    shell(f'xrandr --output {output} --mode {mode}')


def main():
    CliBuilder('completers-demo').has(
        parameter('output', choices=list_screens, required=True),
        parameter('mode', choices=['640x480', '800x480', '800x600'], required=True),
        default_action(adjust_screen),
    ).run()


if __name__ == '__main__':
    main()
```

In order to enable auto-completion, you need to install some extension to bash. Fortunately `cliglue` has built-in tools to do that:
```console
foo@bar:~$ sudo ./completers.py --bash-install completers-demo
[info]  creating link: /usr/bin/completers-demo -> ~/cliglue/doc/example/completers.py
#!/bin/bash
_autocomplete_98246661() {
COMPREPLY=( $(completers-demo --bash-autocomplete "${COMP_LINE}") )
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
--bash-autocomplete  -h                   --mode               --output
--bash-install       --help               --mode=              --output=

foo@bar:~$ completers-demo --mo[Tab]
foo@bar:~$ completers-demo --mode

foo@bar:~$ completers-demo --mode [Tab][Tab]
640x480  800x480  800x600

foo@bar:~$ completers-demo --mode 640[Tab]
foo@bar:~$ completers-demo --mode 640x480

foo@bar:~$ completers-demo --mode 640x480 --output [Tab][Tab]
eDP-1   HDMI-1
```
