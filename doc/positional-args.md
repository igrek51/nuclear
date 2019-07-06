# Positional arguments


TODO

## Positional arguments
(e.g. `git push <origin> <master>`)

```python
Create positional argument rule specification.
Positional argument is an unnamed param
which is recognized by its position in the command line arguments list.
:param name: argument name, which will be used to reference argument value
:param help: description of the argument displayed in help output
:param required: whether positional argument is required.
If it's required but it's not given, the syntax error will be raised.
:param default: default value for the argument, if it's not given (and it's not required)
:param type: type of argument value (e.g. str, int, float)
Reference to a parser function may be provided here as well.
Then argument value is evaluated by passing the string argument value to that function.
:param choices: Explicit list of available choices for the argument value
or reference to a function which will be invoked to retrieve such possible values list.
:return: new positional argument rule specification
```

## All remaining args
docker run cmd example

```python
"""
Create 'All remaining arguments' rule specification.
It allows to retrieve all CLI argumetns, which were not matched before.
All matched arguments will be extracted to a list of arguments or a string (depending on joined_with parameter)
:param name: variable name, which will be used to reference matched arguments list
:param joined_with: optional string joiner for arguments.
If it's set, all matched arguments will be joined to string with that joiner.
It it's not given, matched arguments will be passed as list of strings.
This value (string or list) can be accessed by specified name, when it's being injected to a function.
:return: new all remaining arguments rule specification
"""
```
