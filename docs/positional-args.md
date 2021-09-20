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

