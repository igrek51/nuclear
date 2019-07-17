## Flags
Flag is a boolean parameter which is toggled by single keyword.
There are supported both short (`-f`) and long (`--force`) formats.

In order to create flag rule specification, use:
```python
from cliglue import flag

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

### Multiple flag occurrences
Multiple occurences are also supported for flags. When `multiple` is set to `True`, then the flag value represents how many times it was set. The value type is then `int`, not `bool`.
```python
CliBuilder(run=lambda verbose: print(f'how many times: {verbose}')).has(
    flag('verbose', 'v', multiple=True),
).run()
```

See [flag tests](../tests/parser/test_flag.py) for specification.
