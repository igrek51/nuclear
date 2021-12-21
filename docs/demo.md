## Demo
```python
from nuclear import CliBuilder

cli = CliBuilder()

@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """
    Say hello
    :param decode: Decode name as base64
    """
    message = f"I'm a {b64decode(name).decode() if decode else name}!"
    print(' '.join([message] * repeat))

@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

@cli.add_command('calculate', 'primes')
def calculate_primes(n: int):
    """List prime numbers using Sieve of Eratosthenes"""
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), range(2, n), set(range(2, n)))))

cli.run()
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-live.gif?raw=true)

See [demo.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-decorator.py) for a complete example.

## Get it now
```bash
pip install nuclear
```

## CLI Tree builder
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

