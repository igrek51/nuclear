## Data types
`nuclear` supports typed values for parameters or positional arguments.
By default, all values have string types.
It can be changed by defining `type` parameter.

There are 2 possible `type` values:
- type name itself (e.g. `int`, `str`, `float`)
- reference for a parser which returns a value
In both cases, the internal variable value is calculated by invoking `type(str_value)`.
When argument value has invalid format, there is syntax error raised. 

### Basic types (int, float, etc.)
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

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

foo@bar:~$ ./example.py
[ERROR] Syntax error: required positional argument "count" is not given
Usage:
  ./pyt.py [OPTIONS] COUNT

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
```

### Built-in data types
`nuclear` has built-in parsers / validators for some types

#### boolean type
`boolean` converts string value (eg. `true`, `True`, `1`, `yes`) to Pythonic `bool` type.
```python
from nuclear.cli.types.boolean import boolean

parameter('enabled', type=boolean)
```

#### Filesystem types
- `nuclear.types.filesystem.existing_file` validates if given string is an existing regular file (not a directory).
After validation, the value is internally stored as `str`.
```python
from nuclear.cli.types.filesystem import existing_file

argument('file', type=existing_file)
```

- `nuclear.types.filesystem.existing_directory` validates if given string is an existing directory.
After validation, the value is internally stored as `str`.
```python
from nuclear.cli.types.filesystem import existing_directory

argument('file', type=existing_directory)
```

#### Datetime types
- `nuclear.types.time.iso_date` parses / validates given string as a date in ISO format: `%Y-%m-%d`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.cli.types.time import iso_date

argument('date', type=iso_date)
```

- `nuclear.types.time.iso_time` parses / validates given string as a time in ISO format: `%H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.cli.types.time import iso_time

argument('time', type=iso_time)
```

- `nuclear.types.time.iso_time` parses / validates given string as a datetime in ISO format: `%Y-%m-%d %H:%M:%S`.
After validation, the value is internally stored as `datetime.datetime`.
```python
from nuclear.cli.types.time import iso_datetime

argument('datetime', type=iso_datetime)
```
Example:
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.cli.types.time import iso_datetime
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

foo@bar:~$ ./example.py "2019-07-13 20:00:05"
2019-07-13 20:00:05
```

- `nuclear.types.time.datetime_format` parses / validates given string as a datetime in custom formats specified by user.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.cli.types.time import datetime_format
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

- `nuclear.types.time.today_format` parses / validates given string as a time in custom formats specified by user.
It gets time from input and combines it with the today date.
You may specify multiple formats and the CLI argument will be parsed sequentially for each format.
The first successfully parsed datetime is returned.
After that, the value is internally stored as `datetime.datetime`.

```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument
from nuclear.cli.types.time import today_format
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
#!/usr/bin/env python3
import re
from dataclasses import dataclass
from nuclear import CliBuilder, argument

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

