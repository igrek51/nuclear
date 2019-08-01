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
from cliglue import dictionary

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
from cliglue import CliBuilder, dictionary

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

See [dictionaries tests](https://github.com/igrek51/cliglue/blob/master/tests/parser/test_dictionary.py) for more detailed use cases.

