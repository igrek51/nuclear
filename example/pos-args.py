#!/usr/bin/env python3
from nuclear import CliBuilder, argument


def print_args(remote: str, branch: str):
    print(f'remote: {remote}, argument: {branch}')


def main():
    CliBuilder('pos-args', run=print_args).has(
        argument('remote', help='remote name', type=str, choices=['origin', 'local']),
        argument('branch', help='branch name', required=False, default='master'),
    ).run()


if __name__ == '__main__':
    main()
