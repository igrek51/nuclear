from nuclear import *
from tests.asserts import MockIO
from functools import reduce
import base64


cli = CliBuilder()


@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """
    Say hello to someone.
    :param decode: Decode name as base64
    """
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))


@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))


@cli.add_command('calculate', 'primes')
def calculate_primes(n: int = 100):
    """
    List prime numbers using Sieve of Eratosthenes
    :param n: maximum number to check
    """
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))


def test_calling_subcommand():
    with MockIO('hello', 'world') as mockio:
        cli.run()
        assert mockio.output() == "I'm a world!\n"
    with MockIO('calculate', 'factorial', '6') as mockio:
        cli.run()
        assert mockio.output() == "720\n"
    with MockIO('calculate', 'primes', '-n=10') as mockio:
        cli.run()
        assert mockio.output() == "[2, 3, 5, 7]\n"
