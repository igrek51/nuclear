#!/usr/bin/env python3
from nuclear import CliBuilder, argument, arguments, flag, parameter, subcommand, dictionary


def main():
    CliBuilder('hello-app', version='1.0.0', help='welcome', run=say_hello).has(
        flag('--verbose', '-v', help='verbosity', multiple=True),
        parameter('repeat', 'r', help='how many times', type=int, required=False, default=1, choices=[1, 2, 3, 5, 8]),
        argument('name', help='description', required=False, default='world', type=str, choices=['monty', 'python']),
        arguments('cmd', joined_with=' '),
        subcommand('run', help='runs something').has(
            subcommand('now', 'n', run=lambda cmd: print(f'run now: {cmd}')),
        ),
        dictionary('config', 'c', help='configuration', key_type=str, value_type=int)
    ).run()


def say_hello(name: str, verbose: int, repeat: int, cmd: str, config: dict):
    print(f'Hello {name}')


if __name__ == '__main__':
    main()
