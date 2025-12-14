#!/usr/bin/env python3
from nuclear import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action
from nuclear.cli.types.filesystem import existing_directory
from nuclear.cli.types.time import iso_datetime


def main():
    CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
               with_defaults=True, usage_onerror=False, reraise_error=True).has(
        subcommand('git').has(
            subcommand('push', run=git_push).has(
                argument('remote'),
                argument('branch', required=False),
                flag('-u', '--upstream', help='set upstream'),
            ),
            subcommand('help', help='show help', run=lambda: print('show help')),
            subcommand('checkout', 'co', help='checkout branch').has(
                argument('branch', choices=['master', 'feature', 'develop'], type=str),
                flag('force', 'f'),
            ),
            subcommand('remote', help='show remotes list').has(
                subcommand('set-url', 'rename', help="change remote's name").has(
                    argument('remote-name', choices=['origin', 'backup'], type=str),
                    argument('new-name'),
                ),
            ),
            parameter('--date', type=iso_datetime),
            parameter('--count', type=int, required=True),
            parameter('--work-tree', type=existing_directory, default='.', help='working directory'),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=list_screens),
            flag('primary', 'p'),
            default_action(xrandr_run)
        ),
        subcommand('docker').has(
            subcommand('exec', run=docker_exec).has(
                parameter('-u', name='user', type=int),
                argument('container-name'),
                arguments(name='cmd', joined_with=' '),
            ),
        ),
        default_action(lambda: print('default action')),
    ).run()


def git_push(remote: str, branch: str, upstream: bool):
    print(f'git push: {remote}, {branch}, {upstream}')


def xrandr_run(output, primary):
    print(f'xrandr: {output} {primary}')


def list_screens():
    return ['eDP1', 'HDMI2']


def docker_exec(user: int, container_name: str, cmd: str):
    print(f'docker exec {user}, {container_name}, {cmd}')


if __name__ == '__main__':
    main()
