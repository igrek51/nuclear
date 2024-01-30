## How does it work?

`nuclear` parses and validates the command line arguments
provided by the user when starting a console application.
It then automatically invokes the appropriate action,
based on the declared Command-Line Interface rules, injecting all the necessary  parameters.
You don't need to write the "glue" code to bind & parse the parameters each time.
This makes writing console aplications simpler and clearer.

1. You define CLI rules for your program in a declarative tree using `CliBuilder`.
  Rules can bind your functions to be called later.
2. When running your program in a shell provided with command-line arguments,
  it starts `.run()` which does the parsing.
3. `nuclear` parses and validates all the parameters, flags, sub-commands,
  positional arguments, etc., and stores them internally.
4. `nuclear` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `nuclear` injects all its needed parameters
  based on the previously defined & parsed values.

You just need to bind the keywords with rules and `nuclear` will take care of the rest for you.

