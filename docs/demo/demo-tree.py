#!/usr/bin/env python3
from functools import reduce
from base64 import b64decode

from nuclear import CliBuilder, argument, flag, parameter, subcommand


def main():
    CliBuilder().has(
        subcommand('hello', run=say_hello, help='Say hello').has(
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


def say_hello(name: str, decode: bool, repeat: int):
    message = f"I'm a {b64decode(name).decode() if decode else name}!"
    print(' '.join([message] * repeat))


def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))


def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r),
                        range(2, n), set(range(2, n)))))


if __name__ == '__main__':
    main()
