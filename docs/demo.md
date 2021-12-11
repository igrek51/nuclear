## Demo
```python
#!/usr/bin/env python3
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

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-live.gif?raw=true)

See [demo.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo.py) for a complete example
or [demo-decorator.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-decorator.py)
(if you want to do the same using decorator-based syntax).

## Get it now
```bash
pip install nuclear
```

