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
- [Auto-generated help and usage](#auto-generated-help) (`--help`)
- [Shell autocompletion](#auto-completion) (getting most relevant hints on hitting `Tab`)
- [Multilevel sub-commands](#sub-commands) (e.g. `git remote add ...` syntax)
- [Named parameters](#named-parameters): supporting both `--name value` and `--name=value`
- [Flags](#flags): supporting both short (`-f`) and long (`--force`)
- [Positional arguments](#positional-arguments) (e.g. `git push <origin> <master>`)
- Invoking matched action function & providing corresponding parameters
- [Custom type validators / parsers](#custom-type-parsers)
- [Custom auto-completers](#custom-completers) (providers of possible values)
- [Handling syntax errors, parameters validation](#errors-handling)
- [Typed values](#data-types) (int, time, date, file, etc.)
- Default values for optional arguments
- [Standard options](#clibuilder) enabled by default (`--help`, `--version`)
- [Declarative CLI builder](#cli-rules-cheatsheet)

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

## CliBuilder
`CliBuilder` is a main class of `cliglue` package which allows to build CLI definition.
It's a builder for Command Line Interface specification.
After that, you can invoke `.run()` method in order to parse provided arguments and invoke particular actions.

Empty CliBuilder has standard options enabled by default:
- `--help` - displaying usage and help
- `--version` - displaying application version number (if it has been defined)

### Creating CliBuilder
In this step you can create new `CliBuilder` and set a custom configuration for it.
 The constructor is as follows:
```python
from cliglue import CliBuilder

CliBuilder(
           name: Optional[str] = None,
           version: Optional[str] = None,
           help: Optional[str] = None,
           run: Optional[Action] = None,
           with_defaults: bool = True,
           help_onerror: bool = True,
           reraise_error: bool = False,
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
--bash-install APP-NAME: installing application in bash with autocompleting,
--bash-autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash

`help_onerror` - wheter help output should be displayed on syntax error

`reraise_error` - wheter syntax error should not be caught but reraised instead.
Enabling this causes stack trace to be flooded to the user.

### Declaring CLI rules
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
from cliglue import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action

CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, help_onerror=False, reraise_error=True).has(
    subcommand('checkout'),
    argument('commit'),
    arguments('files'),
    flag('-u', '--upstream', help='set upstream'),
    parameter('--count', type=int, required=True),
    default_action(lambda: print('default action')),
)
```

### Running CLI arguments through parser
The final step is calling `.run()` on `CliBuilder`.
It parses all the CLI arguments passed to application.
Then it invokes triggered action which were defined before.
If actions need some parameters, they will be injected based on the parsed arguments.

Running:
```python
from cliglue import CliBuilder

CliBuilder().run()
```
just prints the standard help output, because it's the default action for an empty builder if no arguments are provided.

## Sub-commands
Commands may form a multilevel tree with nested sub-commands.

Sub-commands syntax is commonly known:
- `git remote rename ...`,
- `docker container ls`,
- `nmcli device wifi list`,
- `ip address show`.

Sub-commands split the CLI into many nested CLI levels, forming a tree.
They decide where to direct the parser, which seeks for a most relevant action to invoke.

Sub-commands create a nested levels of sub-parsers, which not only may have different actions but also contains different CLI rules, such as named parameters, flags or other sub-commands, which are only enabled when parent command is enabled as well.
Subcommand can have more subrules which are activated only when corresponding subcommand is active.
So subcommand is just a keyword which narrows down the context.

### Sub-commands specification
In order to create subcommand rule specification, use:
```python
from cliglue import subcommand

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
from cliglue import CliBuilder, argument, subcommand

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

### Sub-commands example
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

See [sub-commands tests](../tests/parser/test_subcommand.py) for specification.

## Flags
Flag is a boolean parameter which is toggled by single keyword.
There are supported both short (`-f`) and long (`--force`) formats.

In order to create flag rule specification, use:
```python
from cliglue import flag

flag(
        *keywords: str,
        help: str = None,
)
```
`keywords` are arguments (one or many) which any of them enables flag when it occurs.
Flag value is `False` by default.
Flag keywords may be passed using direct format: `-f` or `--flag`,
as well as by name: `f` or `flag`, which will be also evaluated to `-f` or `--flag`.
Single character flags will get single hyphen prefix (`-f`),
longer flag names will get double hyphen prefix (`--flag`).

`help` is description of the flag displayed in help output

Example:
```python
from cliglue import CliBuilder, flag

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

See [flag tests](../tests/parser/test_flag.py) for specification.

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
from cliglue import parameter

parameter(
        *keywords: str,
        name: str = None,
        help: str = None,
        required: bool = False,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
)
```
`keywords` keyword arguments which are matched to parameter.
Parameter keywords may be passed using direct format: '-p' or '--param',
as well as by name: 'p' or 'param', which will be evaluated to '-p' or '--param'.
Single character parameter will get single hyphen prefix (-p),
longer parameter names will get double hyphen prefix (--param)

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

Example:
```python
from cliglue import CliBuilder, parameter

CliBuilder(run=lambda param: print(param)).has(
    parameter('param', 'p'),
).run()
```
Usage:
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

See [parameter tests](../tests/parser/test_param.py) for specification.

## Positional arguments
Positional argument is an unnamed parameter, which is recognized only by its position on their order in command line arguments list.
For example first two arguments (except flags and named parameters) may be detected as positional arguments and matched to corresponding variables.

### Single positional arguments
Let's assume we have CLI syntax: `git push <origin> <master>`.
`git` is application binary name of course, `push` is a sub-command, which have 2 positional arguments: `origin` and `master`.

In order to create positional argument rule specification, use:
```python
from cliglue import argument

def argument(
        name: str,
        help: str = None,
        required: bool = True,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
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

#### Example
**pos-args.py**:
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument


def print_args(remote: str, branch: str):
    print(f'remote: {remote}, argument: {branch}')


def main():
    CliBuilder('pos-args', run=print_args).has(
        argument('remote', help='remote name', type=str, choices=['origin', 'local']),
        argument('branch', help='branch name', required=False, default='master'),
    ).run()


if __name__ == '__main__':
    main()
```
Usage:
```console
foo@bar:~$ ./pos-args.py --help
pos-args

Usage:
  ./pos-args.py [OPTIONS] REMOTE [BRANCH]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

foo@bar:~$ ./pos-args.py
[ERROR] Syntax error: required positional argument "remote" is not given
pos-args

Usage:
  ./pos-args.py [OPTIONS] REMOTE [BRANCH]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

foo@bar:~$ ./pos-args.py origin
remote: origin, argument: master

foo@bar:~$ ./pos-args.py origin develop
remote: origin, argument: develop
```

See [positional arguments tests](../tests/parser/test_positional_argument.py) as a specification.

### Multiple positional arguments
`cliglue` allows to match all remaining (not already matched) arguments.
It can be useful when using syntax like `docker cmd`:
```docker run cmd ubuntu /bin/bash -c /script.sh```
With that syntax all arguments after `ubuntu` - `/bin/bash -c /script.sh` should be matched to one variable. 

You can do it with `cliglue` using `arguments`.
That rule will force parser to store all remaining arguments in a list variable (or in a joined string).

In order to create "all remaining arguments" rule specification, use:
```python
from cliglue import arguments

arguments(
        name: str,
        joined_with: Optional[str] = None,
)
```
It allows to retrieve all CLI argumetns, which were not matched before.
All matched arguments will be extracted to a list of arguments or a string (depending on `joined_with` parameter)

`name` - variable name, which will be used to reference matched arguments list

`joined_with` - optional string joiner for arguments.
If it's set, all matched arguments will be joined to string with that joiner.
It it's not given, matched arguments will be passed as list of strings.
This value (string or list) can be accessed by specified name, when it's being injected to a function.

#### Example
**all-args.py**:
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, arguments, subcommand


def run_cmd(cmd: str):
    print(f'cmd: {cmd}')


def main():
    CliBuilder('all-args').has(
        subcommand('run', run=run_cmd).has(
            arguments('cmd', joined_with=' '),
        ),
    ).run()


if __name__ == '__main__':
    main()
```
Usage:
```console
foo@bar:~$ ./all-args.py
all-args

Usage:
  ./all-args.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  run [CMD...]

Run "./all-args.py COMMAND --help" for more information on a command.

foo@bar:~$ ./all-args.py run /bin/bash -c script.sh
cmd: /bin/bash -c script.sh

foo@bar:~$ ./all-args.py run "/bin/bash -c script.sh"
cmd: /bin/bash -c script.sh
```

See [all arguments tests](../tests/parser/test_all_arguments.py) for specification.

## Auto-completion
Shell autocompletion allows to suggest most relevant hints on hitting `Tab` key.

Auto-completion is enabled by default to all known keywords based on the declared subcommands and options.

Defining possible choices may imporove auto-completing arguments. You can declare explicit possible values list or a function which provides such a list at runtime.

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
With `cliglue` you just need to run:
```console
# sudo ./sample-app.py --bash-install sample-app
```
It will install autocompletion script and add a symbolic link in `/usr/bin/`,
so as you can run your app with `sample-app` command instead of `./sample_app.py`.

Now you can type `sample-app` and hit `Tab` to see what are the possible commands and options.

If you type `sample-app --he`, it will automatically fill the only possible option: `--help`.

Sometimes, you need to make some modifications in your code,
but after these modifications you will NOT need to reinstall autocompletion again.
You had to do it only once, because autocompletion script only redirects its query and run `sample_app.py`:
```console
sample-app --bash-autocomplete "sample-app --he"
```

## Auto-generated help
`cliglue` auto-generates help and usage output based on the defined CLI rules.

Let's say we have quite complex CLI definition:
```python
CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, help_onerror=False, reraise_error=True).has(
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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

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
multiapp v1.0.0
```

## Data types
`cliglue` supports typed values for parameters or positional arguments.
By default, all values have string types.
It can be changed by defining `type` parameter.

There are 2 possible `type` values:
- type name itself (e.g. `int`, `str`, `float`)
- reference for a parser which returns a value
In both cases, the internal variable value is calculated by invoking `type(str_value)`.
When argument value has invalid format, there is syntax error raised. 

### Basic types (int, float, etc.)
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument

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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

foo@bar:~$ ./example.py
[ERROR] Syntax error: required positional argument "count" is not given
Usage:
  ./pyt.py [OPTIONS] COUNT

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals
```

### Built-in data types
`cliglue` has built-in parsers / validators for some types

#### Filesystem types
- `cliglue.types.filesystem.existing_file` validates if given string is an existing regular file (not a directory).
After validation, the value is internally stored as `str`.
```python
from cliglue.types.filesystem import existing_file

argument('file', type=existing_file)
```

- `cliglue.types.filesystem.existing_directory` validates if given string is an existing directory.
After validation, the value is internally stored as `str`.
```python
from cliglue.types.filesystem import existing_directory

argument('file', type=existing_directory)
```

#### Datetime types
- `cliglue.types.time.iso_date` parses / validates given string as a date in ISO format: `%Y-%m-%d`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from cliglue.types.time import iso_date

argument('date', type=iso_date)
```

- `cliglue.types.time.iso_time` parses / validates given string as a time in ISO format: `%H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from cliglue.types.time import iso_time

argument('time', type=iso_time)
```

- `cliglue.types.time.iso_time` parses / validates given string as a datetime in ISO format: `%Y-%m-%d %H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from cliglue.types.time import iso_datetime

argument('datetime', type=iso_datetime)
```
Example:
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument
from cliglue.types.time import iso_datetime
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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

foo@bar:~$ ./example.py "2019-07-13 20:00:05"
2019-07-13 20:00:05
```

- `cliglue.types.time.datetime_format` parses / validates given string as a datetime in custom formats specified by user.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument
from cliglue.types.time import datetime_format
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

- `cliglue.types.time.today_format` parses / validates given string as a time in custom formats specified by user.
It gets time from input and combines it with the today date.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument
from cliglue.types.time import today_format
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
#!/usr/bin/env python3.6
import re
from dataclasses import dataclass
from cliglue import CliBuilder, argument

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
`cliglue` validates passed CLI arguments on running `CliBuilder.run()`

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

`help_onerror` parameter decides wheter help output should be displayed on syntax error.

#### Erros handling example
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument

CliBuilder(help_onerror=False).has(
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
- all remaining arguments rule is defined more than once

#### Wrong CLI Definition example
```python
#!/usr/bin/env python3.6
from cliglue import CliBuilder, argument

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
  File "~/cliglue/cliglue/builder/builder.py", line 69, in run
    self.run_with_args(sys.argv[1:])
  File "~/cliglue/cliglue/builder/builder.py", line 76, in run_with_args
    raise e
  File "~/cliglue/cliglue/builder/builder.py", line 73, in run_with_args
    Parser(self.__subrules).parse_args(args)
  File "~/cliglue/cliglue/parser/parser.py", line 37, in __init__
    self._init_rules()
  File "~/cliglue/cliglue/parser/parser.py", line 57, in _init_rules
    raise CliDefinitionError('argument value may be either required or have the default value')
cliglue.parser.error.CliDefinitionError: argument value may be either required or have the default value
```

## CLI Rules cheatsheet
Here is the cheatsheet for the most important CLI rules:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, arguments, flag, parameter, subcommand


def main():
    CliBuilder('hello-app', run=say_hello).has(
        flag('--force', '-f', help='a flag'),
        parameter('repeat', 'r', help='how many times', type=int, required=False, default=1, choices=[1, 2, 3, 5, 8]),
        argument('name', help='description', required=False, default='world', type=str, choices=['monty', 'python']),
        arguments('cmd', joined_with=' '),
        subcommand('run', help='runs something').has(
            subcommand('now', 'n', run=lambda cmd: print(f'run now: {cmd}')),
        ),
    ).run()


def say_hello(name: str, force: bool, repeat: int, cmd: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    main()
```

## Complex CLI tree
Here's an example of more complex CLI definition tree:

**multiapp.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action
from cliglue.types.filesystem import existing_directory
from cliglue.types.time import iso_datetime


def main():
    CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
               with_defaults=True, help_onerror=False, reraise_error=True).has(
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
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

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

