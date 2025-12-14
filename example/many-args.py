#!/usr/bin/env python3
from nuclear import CliBuilder, arguments, subcommand


def run_cmd(cmd: str):
    print(f'cmd: {cmd}')


def main():
    CliBuilder('all-args').has(
        subcommand('run', run=run_cmd).has(
            arguments('cmd', joined_with=' '),
        ),
    ).run()


if __name__ == '__main__':
    main()
