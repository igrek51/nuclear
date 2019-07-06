# CliBuilder

```python
def __init__(self,
             name: Optional[str] = None,
             version: Optional[str] = None,
             help: Optional[str] = None,
             run: Optional[Action] = None,
             with_defaults: bool = True,
             help_onerror: bool = True,
             reraise_error: bool = False,
             ):
    """
    A builder for Command Line Interface specification
    :param name: name of the application for which the CLI is built
    :param version: application version (displayed in help/version output)
    :param help: short description of application
    :param run: reference for a function which should be the default action for empty arguments list
    :param with_defaults: whether default rules and actions should be added.
    Defaults options are:
    -h, --help: displaying help,
    --version: displaying version,
    --bash-install APP-NAME: installing application in bash with autocompleting,
    --bash-autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash
    :param help_onerror: wheter help output should be displayed on syntax error
    :param reraise_error: wheter syntax error should not be caught but reraised instead.
    Enabling this causes stack trace to be flooded to the user.
    """
```

```python
def has(self, *subrules: CliRule) -> 'CliBuilder':
    """
    Add more CLI rules for the particular level
    :param subrules: Command Line Interface rules,
    such as: subcommands, flags, parameters, options, arguments, default action
    :return: CliBuilder itself for the further building
    """

def run(self):
    """
    Parse all the CLI arguments passed to application.
    Then invoke triggered action which were defined before.
    If actions need some parameters, they will be injected based on the parsed arguments.
    """
```

TODO
- Standard options enabled by default (`--help`, `--version`)
- clibuilder settings