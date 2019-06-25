from cliglue.builder import *
from tests.asserts import MockIO, assert_system_exit, assert_error


def list_screens():
    return ['HDMI', 'eDP']


def test_no_match():
    with MockIO('--bash-autocomplete', 'nomatch') as mockio:
        CliBuilder().run()
        assert mockio.output() == '\n'


def test_empty_builder_proposals():
    with MockIO('--bash-autocomplete', '""') as mockio:
        CliBuilder(with_defaults=True).run()
        assert '-h\n' in mockio.output()
        assert '--help\n' in mockio.output()
        assert '--version\n' in mockio.output()
        assert '--bash-install\n' in mockio.output()
        assert '--bash-autocomplete\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"nomatch "') as mockio:
        CliBuilder(with_defaults=True).run()
        assert '--help\n' in mockio.output()


def test_autocomplete_subcommands():
    def cli_subcommands():
        return CliBuilder(with_defaults=False).has(
            subcommand('git').has(
                subcommand('push'),
                subcommand('remote').has(
                    subcommand('set-url', 'rename'),
                ),
            ),
            subcommand('xrandr'),
        )
    with MockIO('--bash-autocomplete', '') as mockio:
        cli_subcommands().run()
        assert 'git\n' in mockio.output()
        assert 'xrandr\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"nomatch "') as mockio:
        cli_subcommands().run()
        assert 'git\n' in mockio.output()
        assert 'xrandr\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"g"') as mockio:
        cli_subcommands().run()
        assert mockio.output() == 'git\n'
    with MockIO('--bash-autocomplete', '"git"') as mockio:
        cli_subcommands().run()
        assert mockio.output() == 'git\n'
    with MockIO('--bash-autocomplete', '"git "') as mockio:
        cli_subcommands().run()
        assert 'push\n' in mockio.output()
        assert 'remote\n' in mockio.output()
        assert 'git\n' not in mockio.output()
        assert 'xrandr\n' not in mockio.output()
    with MockIO('--bash-autocomplete', '"git remote "') as mockio:
        cli_subcommands().run()
        assert mockio.output() == 'set-url\n'


def test_autocomplete_flags():
    def cli_flags():
        return CliBuilder(with_defaults=False).has(
            subcommand('sub').has(
                flag('--flag-local'),
            ),
            flag('--flag-global'),
        )
    with MockIO('--bash-autocomplete', '') as mockio:
        cli_flags().run()
        assert '--flag-global\n' in mockio.output()
        assert '--flag-local\n' not in mockio.output()
    with MockIO('--bash-autocomplete', 'sub ') as mockio:
        cli_flags().run()
        assert '--flag-global\n' in mockio.output()
        assert '--flag-local\n' in mockio.output()


def test_autocomplete_parameters():
    def cli_parameters():
        return CliBuilder(with_defaults=False).has(
            subcommand('sub').has(
                parameter('--param-local'),
            ),
            parameter('--param-global'),
        )
    with MockIO('--bash-autocomplete', '') as mockio:
        cli_parameters().run()
        assert '--param-global\n' in mockio.output()
        assert '--param-local\n' not in mockio.output()
    with MockIO('--bash-autocomplete', 'sub ') as mockio:
        cli_parameters().run()
        assert '--param-global\n' in mockio.output()
        assert '--param-local\n' in mockio.output()


def test_autocomplete_parameters_choice():
    def cli_parameters():
        return CliBuilder(with_defaults=False).has(
            subcommand('sub').has(
                parameter('--parameter', choices=list_screens),
            ),
        )
    with MockIO('--bash-autocomplete', '"sub --param"') as mockio:
        cli_parameters().run()
        assert mockio.output() == '--parameter\n'
    with MockIO('--bash-autocomplete', '"sub --parameter"') as mockio:
        cli_parameters().run()
        assert '--parameter\n' in mockio.output()
        assert '--parameter=\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"sub --parameter "') as mockio:
        cli_parameters().run()
        assert 'HDMI\n' in mockio.output()
        assert 'eDP\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"sub --parameter H"') as mockio:
        cli_parameters().run()
        assert mockio.output() == 'HDMI\n'
    with MockIO('--bash-autocomplete', '"sub --parameter="') as mockio:
        cli_parameters().run()
        assert '--parameter=HDMI\n' in mockio.output()
        assert '--parameter=eDP\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"sub --parameter=H"') as mockio:
        cli_parameters().run()
        assert mockio.output() == '--parameter=HDMI\n'


def test_autocomplete_pos_arguments_choice():
    def cli_parameters():
        return CliBuilder(with_defaults=False).has(
            subcommand('sub').has(
                argument('pos', choices=['abc', 'def']),
            ),
        )
    with MockIO('--bash-autocomplete', '"sub pos "') as mockio:
        cli_parameters().run()
        assert 'abc\n' in mockio.output()
        assert 'def' in mockio.output()
    with MockIO('--bash-autocomplete', '"sub pos a"') as mockio:
        cli_parameters().run()
        assert 'abc\n' in mockio.output()
        assert 'def' not in mockio.output()


def test_autocomplete_command_last_word_space():
    with MockIO('--bash-autocomplete', 'app info age') as mockio:
        CliBuilder(with_defaults=False).has(
            subcommand('info').has(
                subcommand('age'),
            ),
        ).run()
        assert 'age\n' in mockio.output()
