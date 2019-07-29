from cliglue import *
from cliglue.parser.error import CliSyntaxError
from tests.asserts import MockIO, assert_error


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
                arguments(name='cmd', joined_with=' '),
            ),
            primary_option('--help', '-h'),
        ),
        argument('name'),
        argument('surname', required=False, default=''),
        flag('force'),
    )


def noop():
    pass


def test_default_print_help_empty():
    with MockIO('--help') as mockio:
        CliBuilder(with_defaults=True).run()
        assert 'Usage' in mockio.output()


def test_root_help():
    with MockIO('--help') as mockio:
        build_builder().run()
        assert 'helpgen v1.0.0' in mockio.output()
        assert 'Usage:' in mockio.output()
        assert 'Options:' in mockio.output()
        assert 'Commands:' in mockio.output()
        assert 'Commands:' in mockio.output()

        assert '-h, --help' in mockio.output()
        assert 'Display this help and exit' in mockio.output()
        assert '--version' in mockio.output()

        assert 'git remote rename|set-url' in mockio.output()
        assert 'change remote\'s name' in mockio.output()


def test_subcommand_help():
    with MockIO('git', '--help') as mockio:
        build_builder().run()
        assert 'Usage:' in mockio.output()
        assert 'git [COMMAND]' in mockio.output()
        assert 'xrandr' not in mockio.output()


def test_3rd_level_help():
    with MockIO('git', 'push', '--help') as mockio:
        CliBuilder().has(
            subcommand('git', run=noop).has(
                subcommand('push', run=noop).has(
                    subcommand('remote', run=noop),
                ),
                subcommand('bad', run=noop)
            ),
            subcommand('bad', run=noop)
        ).run()
        assert 'Usage:' in mockio.output()
        assert 'git push [COMMAND]' in mockio.output()
        assert 'remote' in mockio.output()
        assert 'bad' not in mockio.output()


def test_print_help_on_syntax_error():
    with MockIO('--param') as mockio:
        cli = CliBuilder(usage_onerror=True, reraise_error=True).has(
            parameter('param'),
        )
        assert_error(lambda: cli.run(), error_type=CliSyntaxError)
        assert 'Usage:' in mockio.output()


def test_default_help_when_no_arguments():
    with MockIO('') as mockio:
        CliBuilder().run()
        assert 'Usage:' in mockio.output()


def test_hiding_internal_options():
    with MockIO('--help') as mockio:
        CliBuilder(hide_internal=True).run()
        assert '--bash-install' not in mockio.output()
        assert '--bash-autocomplete' not in mockio.output()
    with MockIO('--help') as mockio:
        CliBuilder(hide_internal=False).run()
        assert '--bash-install' in mockio.output()
        assert '--bash-autocomplete' in mockio.output()


def test_omit_empty_subcommands():
    with MockIO('--help') as mockio:
        CliBuilder().has(
            subcommand('show-help', help='shows help'),
            subcommand('push', run=lambda: print('push')),
            subcommand('noop'),
            subcommand('dooo').has(
                subcommand('nothing'),
            ),
            subcommand('do2').has(
                subcommand('it', run=lambda: print('do2 it')),
            ),
        ).run()
        assert 'show-help' in mockio.output()
        assert 'push' in mockio.output()
        assert 'noop' not in mockio.output()
        assert 'dooo' not in mockio.output()
        assert 'nothing' not in mockio.output()
        assert 'do2  ' not in mockio.output()
        assert 'do2 it' in mockio.output()


def test_display_dictionary():
    with MockIO('--help') as mockio:
        CliBuilder().has(
            dictionary('-c', '--config'),
        ).run()
        assert '--config' in mockio.output()


def test_usage_on_syntax_error():
    with MockIO('') as mockio:
        CliBuilder(usage_onerror=True, reraise_error=False).has(
            argument('req')
        ).run()
        assert 'Syntax error' in mockio.output()
        assert '--help" for more information' in mockio.output()


def test_display_explicit_param_name():
    with MockIO('--help') as mockio:
        CliBuilder().has(
            parameter('p', name='param'),
        ).run()
        assert '-p PARAM' in mockio.output()
