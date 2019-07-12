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

