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

#### Example: pos-args.py
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument


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

#### Example: all-args.py
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, arguments, subcommand


def run_cmd(cmd: str):
    print(f'cmd: {cmd}')


CliBuilder('all-args').has(
    subcommand('run', run=run_cmd).has(
        arguments('cmd', joined_with=' '),
    ),
).run()
```
Usage:
```console
foo@bar:~$ ./all-args.py
all-args

Usage:
  ./all-args.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

Commands:
  run [CMD...]

Run "./all-args.py COMMAND --help" for more information on a command.

foo@bar:~$ ./all-args.py run /bin/bash -c script.sh
cmd: /bin/bash -c script.sh

foo@bar:~$ ./all-args.py run "/bin/bash -c script.sh"
cmd: /bin/bash -c script.sh
```

See [all arguments tests](../tests/parser/test_many_arguments.py) for specification.

