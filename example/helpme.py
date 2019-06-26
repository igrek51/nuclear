#!/usr/bin/env python3
from cliglue import types
from cliglue.builder import *


def say_hello(name: str, surname: str, force: bool):
    print('Hello {} {}'.format(name, surname))
    if force:
        print('May the Force be with you!')


def main():
    CliBuilder('helpgen', version='1.0.0', run=say_hello).has(
        subcommand('git').has(
            subcommand('help', help='shows help'),
            subcommand('push').has(
                argument('remote'),
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
            parameter('--work-tree', type=types.existing_directory, default='.'),
            parameter('--config-file', type=types.existing_file),
            parameter('--count', type=int),
            primary_option('-c').has(
                argument('key-value'),
            ),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=['HDMI', 'eDP1']),
            flag('--primary'),
        ),
        subcommand('docker').has(
            subcommand('exec').has(
                flag('--it'),
                parameter('-u', name='user'),
                all_arguments(name='cmd', joined_with=' '),
            ),
            primary_option('--help', '-h'),
        ),
        argument('name'),
        argument('surname', required=False, default=''),
        flag('force'),
    ).run()


if __name__ == '__main__':
    main()
