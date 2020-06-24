## Errors handling
`nuclear` validates passed CLI arguments on running `CliBuilder.run()`

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

`usage_onerror` parameter decides wheter usage output should be displayed on syntax error.

#### Erros handling example
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

CliBuilder(usage_onerror=False).has(
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
- parameter / argument value does not belong to strict available choices list

#### Wrong CLI Definition example
```python
#!/usr/bin/env python3
from nuclear import CliBuilder, argument

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
  File "~/nuclear/nuclear/builder/builder.py", line 69, in run
    self.run_with_args(sys.argv[1:])
  File "~/nuclear/nuclear/builder/builder.py", line 76, in run_with_args
    raise e
  File "~/nuclear/nuclear/builder/builder.py", line 73, in run_with_args
    Parser(self.__subrules).parse_args(args)
  File "~/nuclear/nuclear/parser/parser.py", line 37, in __init__
    self._init_rules()
  File "~/nuclear/nuclear/parser/parser.py", line 57, in _init_rules
    raise CliDefinitionError('argument value may be either required or have the default value')
nuclear.parser.error.CliDefinitionError: argument value may be either required or have the default value
```

