#!/usr/bin/env python3
from functools import reduce
import base64

from nuclear import CliBuilder


cli = CliBuilder()


@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """Say hello to someone"""
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))


@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))


@cli.add_command('calculate', 'primes')
def calculate_primes(n: int = 100):
    """List prime numbers using Sieve of Eratosthenes"""
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))


if __name__ == '__main__':
    cli.run()
