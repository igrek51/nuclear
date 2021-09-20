## CLI Builder
`CliBuilder` is a main class of `nuclear` package which allows to build CLI definition.
It's a builder for Command Line Interface specification.
After that, you can invoke `.run()` method in order to parse provided arguments and invoke particular actions.

Empty CliBuilder has standard options enabled by default:

- `--help` - displaying usage and help
- `--version` - displaying application version number (if it has been defined)

### Step 1. Creating CliBuilder
In this step you can create new `CliBuilder` and set a custom configuration for it.
 The constructor is as follows:
```python
from nuclear import CliBuilder

CliBuilder(
           name: Optional[str] = None,
           version: Optional[str] = None,
           help: Optional[str] = None,
           run: Optional[Action] = None,
           with_defaults: bool = True,
           usage_onerror: bool = True,
           reraise_error: bool = False,
           hide_internal: bool = True,
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
--install-bash APP-NAME: installing application in bash with autocompleting,
--autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash

`usage_onerror` - wheter usage output should be displayed on syntax error

`reraise_error` - wheter syntax error should not be caught but reraised instead.
Enabling this causes stack trace to be flooded to the user.

`hide_internal` - wheter internal options (`--install-bash`, `--autocomplete`) should be hidden on help output.

### Step 2. Declaring CLI rules
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
from nuclear import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action

CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, usage_onerror=False, reraise_error=True).has(
    subcommand('checkout'),
    argument('commit'),
    arguments('files'),
    flag('-u', '--upstream', help='set upstream'),
    parameter('--count', type=int, required=True),
    default_action(lambda: print('default action')),
)
```

### Step 3. Running CLI arguments through parser
The final step is calling `.run()` on `CliBuilder`.
It parses all the CLI arguments passed to application.
Then it invokes triggered action which were defined before.
If actions need some parameters, they will be injected based on the parsed arguments.

Running empty builder:
```python
from nuclear import CliBuilder

CliBuilder().run()
```
just prints the standard help output, because it's the default action for an empty builder if no arguments are provided.

