# CLI Tree builder

*Nuclear* is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

Apart from decorator syntax style, you can also do the same using tree-builder syntax,
which is useful in more complex cases:

```python
from nuclear import CliBuilder, argument, flag, parameter, subcommand

CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        parameter('repeat', type=int, default=1),
        flag('decode', help='Decode name as base64'),
    ),
    subcommand('calculate').has(
        subcommand('factorial', run=calculate_factorial,
                   help='Calculate factorial').has(
            argument('n', type=int),
        ),
        subcommand('primes', run=calculate_primes,
                   help='List prime numbers using Sieve of Eratosthenes').has(
            argument('n', type=int, required=False, default=100,
                     help='maximum number to check'),
        ),
    ),
).run()
```

See [demo-tree.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-tree.py) for a complete example.

