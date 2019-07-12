## Features
- [Auto-generated help and usage](#auto-generated-help) (`--help`)
- [Shell autocompletion](#auto-completion) (getting most relevant hints on hitting `Tab`)
- [Multilevel sub-commands](#sub-commands) (e.g. `git remote add ...` syntax)
- [Named parameters](#named-parameters): supporting both `--name value` and `--name=value`
- [Flags](#flags): supporting both short (`-f`) and long (`--force`)
- [Positional arguments](#positional-arguments) (e.g. `git push <origin> <master>`)
- Invoking matched action function & providing corresponding parameters
- [Custom type validators / parsers](#custom-type-parsers)
- [Custom auto-completers](#custom-completers) (providers of possible values)
- [Handling syntax errors, parameters validation](#errors-handling)
- [Typed values](#data-types) (int, time, date, file, etc.)
- Default values for optional arguments
- [Standard options](#clibuilder) enabled by default (`--help`, `--version`)
- [Declarative CLI builder](#cli-rules-cheatsheet)

