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
        strict_choices: bool = False,
        multiple: bool = False,
)
```
`keywords` keyword arguments which are matched to parameter.
Parameter keywords may be passed using direct format: `-p` or `--param`,
as well as by name: `p` or `param`, which will be evaluated to `-p` or `--param`.
Single character parameter will get single hyphen prefix (`-p`),
longer parameter names will get double hyphen prefix (`--param`)

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

`strict_choices` - whether given arguments should be validated against available choices

`multiple` - whether parameter is allowed to occur many times.
Then parameter has list type and stores list of values

Basic parameter example:
```python
from cliglue import CliBuilder, parameter

CliBuilder(run=lambda param: print(param)).has(
    parameter('param', 'p'),
).run()
```
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

### Multiple parameter occurrences
Multiple occurences are also supported for parameters.
When `multiple` is set to `True`, then the parameter value represents list of values and can be appended mutliple times.
The value type is then `list`.
```python
def what_to_skip(skip: List[str]):
    print(f'skipping: {skip}')

CliBuilder(run=what_to_skip).has(
    parameter('skip', multiple=True, type=str),
).run()
```
```console
foo@bar:~$ ./example.py --skip build --skip run
skipping: ['build', 'run']
``` 

See [parameter tests](https://github.com/igrek51/cliglue/blob/master/tests/parser/test_param.py) for more detailed use cases.

