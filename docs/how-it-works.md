## Example

```python
from nuclear import CliBuilder, argument, flag, parameter, subcommand

CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        flag('decode', help='Decode name as base64'),
        parameter('repeat', type=int, default=1),
    ),
    subcommand('calculate').has(
        subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
            argument('n', type=int),
        ),
        subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
            argument('n', type=int, required=False, default=100, help='maximum number to check'),
        ),
    ),
).run()
```

## How does it work?
1. You define all required CLI rules for your program in a declarative tree.
2. User provides command-line arguments when running program in a shell.
3. `nuclear` parses and validates all the parameters, flags, sub-commands, positional arguments, etc, and stores them internally.
4. `nuclear` finds the most relevant action (starting from the most specific) and invokes it.
5. When invoking a function, `nuclear` injects all its needed parameters based on the previously defined & parsed values.

You only need to bind the keywords to the rules and `nuclear` will handle all the rest for you.

