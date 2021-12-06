#!/usr/bin/env python3
from functools import reduce
import base64

from nuclear import CliBuilder, argument, flag, parameter, subcommand


# def main():
#     CliBuilder().has(
#         subcommand('hello', run=say_hello).has(
#             argument('name'),
#             parameter('repeat', type=int, default=1),
#             flag('decode', help='Decode name as base64'),
#         ),
#         subcommand('calculate').has(
#             subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
#                 argument('n', type=int),
#             ),
#             subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
#                 argument('n', type=int, required=False, default=100,
#                          help='maximum number to check'),
#             ),
#         ),
#     ).run()


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
    print(sorted(reduce((lambda r, x: r - set(range(x ** 2, n, x)) if (x in r) else r),
                        range(2, int(n ** 0.5)), set(range(2, n)))))


if __name__ == '__main__':
    cli.run()
