#!/usr/bin/env python3
from nuclear import CliBuilder, subcommand


def main():
    CliBuilder('subcommands-demo').has(
        subcommand('remote', run=lambda: print('action remote'), help='List remotes').has(
            subcommand('push', run=lambda: print('action remote push')),
            subcommand('rename', run=lambda: print('action remote rename')),
        ),
        subcommand('checkout', run=lambda: print('action checkout'), help='Switch branches'),
        subcommand('branch', run=lambda: print('action branch'), help='List branches'),
    ).run()


if __name__ == '__main__':
    main()
