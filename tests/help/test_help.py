from cliglue.builder import *
from tests.asserts import MockIO, assert_system_exit


def build_builder() -> CliBuilder:
    return CliBuilder('helpgen', version='1.0.0', help='tool for generating help').has(
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
            parameter('--count', type=int),
            primary_option('--exit')
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
    )


def test_default_print_help_empty():
    with MockIO() as mockio:
        CliBuilder().run()
        assert 'Usage' in mockio.output()


def test_root_help():
    with MockIO() as mockio:
        build_builder().print_help([])
        assert 'helpgen v1.0.0' in mockio.output()
        assert 'Usage:' in mockio.output()
        assert 'Options:' in mockio.output()
        assert 'Commands:' in mockio.output()
        assert 'Commands:' in mockio.output()

        assert '-h, --help' in mockio.output()
        assert 'Display this help and exit' in mockio.output()
        assert '--bash-install' in mockio.output()
        assert '--version' in mockio.output()

        assert 'git remote rename|set-url' in mockio.output()
        assert 'change remote\'s name' in mockio.output()
