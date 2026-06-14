#!/usr/bin/env python3
from livekey import animate_commands


commands = [
    './demo.py hello Nuclear',
    './demo.py',
    './demo.py calculate --help',
    './demo.py calculate factorial 6',
    './demo.py calculate primes 100',
    './demo.py hello --help',
    './demo.py hello --repeat 3 --decode UGlja2xl',
]


if __name__ == '__main__':
    animate_commands(commands)
