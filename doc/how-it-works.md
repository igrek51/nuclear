## How does it work?
1. You define all required CLI rules for your program in a declarative tree.
2. User provides command-line arguments when running program in a shell.
3. `cliglue` parses and validates all the parameters, flags, sub-commands, positional arguments, etc.
4. `cliglue` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `cliglue` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `cliglue` will handle all the rest for you.

