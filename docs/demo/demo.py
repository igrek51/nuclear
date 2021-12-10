#!/usr/bin/env python3
from functools import reduce
import base64

from nuclear import CliBuilder, argument, flag, parameter, subcommand


def main():
    CliBuilder().has(
        subcommand('hello', run=say_hello).has(
            argument('name'),
            parameter('repeat', type=int, default=1),
            flag('decode', help='Decode name as base64'),
        ),
        subcommand('calculate').has(
            subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
                argument('n', type=int),
            ),
            subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
                argument('n', type=int, required=False, default=100,
                         help='maximum number to check'),
            ),
        ),
    ).run()


def say_hello(name: str, decode: bool, repeat: int):
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))


def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))


def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))


if __name__ == '__main__':
    main()
