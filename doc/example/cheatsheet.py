#!/usr/bin/env python3
from cliglue import CliBuilder, argument, arguments, flag, parameter, subcommand


def main():
    CliBuilder('hello-app', version='1.0.0', help='welcome', run=say_hello).has(
        flag('--force', '-f', help='a flag'),
        parameter('repeat', 'r', help='how many times', type=int, required=False, default=1, choices=[1, 2, 3, 5, 8]),
        argument('name', help='description', required=False, default='world', type=str, choices=['monty', 'python']),
        arguments('cmd', joined_with=' '),
        subcommand('run', help='runs something').has(
            subcommand('now', 'n', run=lambda cmd: print(f'run now: {cmd}')),
        ),
    ).run()


def say_hello(name: str, force: bool, repeat: int, cmd: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    main()
