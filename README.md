# cliglue - Binding glue for CLI

[![Build Status](https://travis-ci.org/igrek51/cliglue.svg?branch=master)](https://travis-ci.org/igrek51/cliglue)

`cliglue` is a declarative parser for command line interfaces in Python.
It's a glue between CLI shell arguments and functions being invoked.

`cliglue` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the 'glue' code for binding & parsing parameters every time.
So it makes writing console aplications faster and simpler.

## Features
- Auto-generated help and usage message (`--help`)
- Generated shell autocompletion (getting most relevant hints on hitting `Tab`)
- Multilevel sub-commands (e.g. `git remote add ...`)
- Named parameters - supporting both `--name value` and `--name=value`
- Flags - supporting both short (`-f`) and long (`--force`)
- Positional arguments (e.g. `git push <origin> <master>`)
- Invoking matched action function with parameters injected
- Custom type validators / parsers
- Custom auto-completers (providers of possible values)
- Typed values (int, time, date, file, etc.)
- Default values for optional arguments
- Standard options enabled by default (`--help`, `--version`)
- Parameters validation, handling syntax errors

## Quick start
Let's create simple command-line application using `cliglue`.
Let's assume we have a function as follows:
```python
def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)
```
and we want it to be run with different parameters provided by user in a terminal shell.

We need a glue which binds it with a CLI:

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
- `CliBuilder` is used to build CLI tree for application.
- `'hello-app'` is a name for that console application to be displayed in help output.
- `run=say_hello` sets default action for the application. Now a function `say_hello` is binded as a main action.
- `.has(...)` allows to embed other rules inside that builder.
- `argument('name')` adds positional argument. From now, first argument (after binary name) will be recognized as `'name'` variable.
- `flag('reverse')` binds '--reverse' keyword to a flag named 'reverse'. So as it may be used later on.
- `parameter('repeat', type=int, default=1)` binds '--repeat' keyword to a parameter named 'repeat', which type is `int` and its default value is `1`.

Finally, invoking `.run()` does all the magic.
It gets system arguments list and starts to process them.

### Help
`CliBuilder` has some basic options added by default, like `--help` or `--version`.
You can check the usage by running application with `--help` flag:
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

Notice there are already rules being displayed, which we declared before:
- positional argument `name`: `./hello.py [OPTIONS] NAME`
- flag `reverse`: `--reverse`
- parameter `repeat`: `--repeat REPEAT`

### Injecting parameters

So when we execute our application with one argument provided, we get:
```console
foo@bar:~$ ./hello.py world
Hello world.
```
and it is matched to `name` argument.
We've binded `say_hello` as a default action, so it has been invoked with particular parameters:
```python
say_hello(name='world', reverse=False, repeat=1)
```
- `name` positional argument has been assigned a `'world'` value.
- `reverse` flag was not given, so it's `False` by default.
- `repeat` parameter was not given either, so it was set to its default value `1`.

Let's provide all of the parameters, then we get:
```console
foo@bar:~$ ./hello.py --reverse world --repeat 2
Hello dlrow.Hello dlrow.
```
Or we can do the same with different syntax:
```console
foo@bar:~$ ./hello.py world --repeat=2 --reverse
Hello dlrow.Hello dlrow.
```

## More examples

### Sub-commands
Commands may build a multilevel tree with nested sub-commands (similar to `git`, `nmcli` or `ip` syntax).

**subcommands.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, subcommand


def main():
    CliBuilder('subcommands').has(
        subcommand('remote').has(
            subcommand('push', run=lambda: print('action remote push')),
            subcommand('rename', run=lambda: print('action remote rename')),
        ),
        subcommand('checkout', run=lambda: print('action checkout')),
        subcommand('branch', run=lambda: print('action branch')),
    ).run()


if __name__ == '__main__':
    main()
```
Usage:
```console
foo@bar:~$ ./subcommands.py remote push
action remote push
```

### Auto-completion
Defining choices may help in auto-completing arguments. You can declare explicit possible values list or a function which provides such a list at runtime.

**completers.py**:
```python
#!/usr/bin/env python3
import re
from typing import List

from cliglue import CliBuilder, parameter, default_action
from cliglue.utils.shell import shell_output


def list_screens() -> List[str]:
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def main():
    CliBuilder('completers-demo').has(
        parameter('output', choices=list_screens),
        parameter('mode', choices=['640x480', '800x480', '800x600']),
        default_action(lambda: print('\n'.join(list_screens()))),
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
We can hit `Tab` key to complete command when typing:
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

TODO more examples

## How does it work?
- You define all required CLI rules for your program in a declarative tree.
- User provides command-line arguments when running program in a shell
- `cliglue` parses and validates all the parameters, flags, sub-commands, positional arguments, etc.
- `cliglue` finds the most relevant action and invokes it
- When invoking a function, `cliglue` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `cliglue` will handle all the rest for you.

## `cliglue` vs `argparse`
Why `cliglue`, since we already have Python `argparse`? Here are some subjective advantages of `cliglue`:
- declarative way of CLI logic
- autocompletion
- easier way of building multilevel sub-commands
- easier & simpler CLI building and documenting it
- auto action binding & injecting arguments, no need to pass `args` to functions manually


## Installation

### Requirements
Install Python 3.6 (or newer)
#### Ubuntu
```console
sudo apt install python3.6
```
#### Centos
```console
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
```
#### Debian
```console
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xvf Python-3.6.9.tgz
cd Python-3.6.3
./configure --enable-optimizations
make -j8
sudo make altinstall
```

### Install package using pip
Install package from [PyPI repository](https://pypi.org/project/cliglue) using pip:
```console
# apt install python3-pip # for Debian
# pip3 install cliglue
```

### Install package in develop mode
Clone repo and install dependencies:
```bash
pip3 install -r requirements.txt
```
Then install package in develop mode:
```bash
python3 setup.py develop
```

## Testing
Running tests:
```bash
pip3 install -r requirements.txt -r requirements-test.txt
./pytest.sh
```
