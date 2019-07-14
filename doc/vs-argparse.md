## `cliglue` vs `argparse`
Why to use `cliglue`, since we already have Python `argparse`? Here are some subjective advantages of `cliglue`:
- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building - when reading the code, it's easier to distinguish particular CLI rules between them (i.e. flags from positional arguments, parameters or sub-commands),
- CLI definition code as a clear documentation.

### Migrating from `argparse` to `cliglue`
TODO 
TODO referencing by function reference, not string name

