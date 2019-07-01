#!/usr/bin/env python3
from cliglue import CliBuilder, subcommand


def main():
    CliBuilder('subcommands-demo').has(
        subcommand('remote').has(
            subcommand('push', run=lambda: print('remote push')),
            subcommand('rename', run=lambda: print('remote rename')),
        ),
        subcommand('checkout', run=lambda: print('action checkout')),
        subcommand('branch', run=lambda: print('action branch')),
    ).run()


if __name__ == '__main__':
    main()
