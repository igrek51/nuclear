#!/usr/bin/env python3
from nuclear import CliBuilder, argument, parameter, flag, subcommand, arguments, dictionary
from nuclear.cli.types.filesystem import existing_directory, existing_file


def main():
    CliBuilder('helpgen', version='1.0.0').has(
        subcommand('git').has(
            subcommand('help', help='shows help'),
            subcommand('push').has(
                argument('remote', 'remote repo name'),
                argument('branch', required=False),
            ),
            subcommand('describe').has(
                flag('--tags', help='show tags'),
            ),
            subcommand('checkout').has(
                argument('branch', choices=['1', '2', '3'], type=str),
                flag('force', '-f'),
            ),
            subcommand('remote', help='show remotes list').has(
                subcommand('set-url', 'rename', help='change remote\'s name').has(
                    argument('remote-name', choices=['1', '2', '3'], type=str),
                    argument('new-name'),
                ),
                flag('force', '-f', help='ignore warnings'),
            ),
            parameter('--work-tree', type=existing_directory, default='.'),
            parameter('--config-file', type=existing_file),
            parameter('--count', type=int),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=['HDMI', 'eDP1']),
            flag('--primary'),
        ),
        subcommand('docker').has(
            subcommand('exec').has(
                flag('--it'),
                parameter('-u', name='user'),
                arguments(name='cmd', joined_with=' '),
            ),
        ),
        flag('force'),
        dictionary('-c', '--config'),
    ).run()


if __name__ == '__main__':
    main()
