## Features
- [Auto-generated help and usage](#auto-generated-help) (`--help`)
- [Shell autocompletion](#auto-completion) (getting most relevant hints on hitting `Tab`)
- [Multilevel sub-commands](#sub-commands) (e.g. `git remote add ...` syntax)
- [Named parameters](#named-parameters): supporting both `--name value` and `--name=value`, multiple parameter occurrences
- [Flags](#flags): supporting both short (`-f`) and long (`--force`), multiple flag occurrences
- [Positional arguments](#positional-arguments) (e.g. `git push <origin> <master>`)
- [Invoking matched action function & injecting parameters](#injecting-parameters)
- [Custom type validators / parsers](#custom-type-parsers)
- [Custom auto-completers](#custom-completers) (providers of possible values)
- [Handling syntax errors, parameters validation](#errors-handling)
- [Typed values](#data-types) (int, time, date, file, etc.)
- [Standard options](#clibuilder) enabled by default (`--help`, `--version`)
- [Declarative CLI builder](#cli-rules-cheatsheet)

