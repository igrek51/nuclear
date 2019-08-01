## Many positional arguments
`cliglue` allows to match all remaining (not already matched) arguments.
It can be useful when using syntax like `docker cmd`:
```docker run cmd ubuntu /bin/bash -c /script.sh```
With that syntax all arguments after `ubuntu` - `/bin/bash -c /script.sh` should be matched to one variable. 

You can do it with `cliglue` using `arguments`.
That rule will force parser to store all remaining arguments in a list variable (or in a joined string).

In order to create "multiple arguments" rule specification, use:
```python
from cliglue import arguments

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
from cliglue import CliBuilder, arguments, subcommand


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

See [many arguments tests](https://github.com/igrek51/cliglue/blob/master/tests/parser/test_many_arguments.py) for more detailed use cases.

