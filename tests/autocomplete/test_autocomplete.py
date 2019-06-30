from cliglue import *
from tests.asserts import MockIO


def list_screens():
    return ['HDMI', 'eDP']


def test_no_match():
    with MockIO('--bash-autocomplete', 'app nomatch') as mockio:
        CliBuilder().run()
        assert mockio.output() == '\n'


def test_empty_builder_proposals():
    with MockIO('--bash-autocomplete', 'app ') as mockio:
        CliBuilder(with_defaults=True, version='1').run()
        assert '-h\n' in mockio.output()
        assert '--help\n' in mockio.output()
        assert '--version\n' in mockio.output()
        assert '--bash-install\n' in mockio.output()
        assert '--bash-autocomplete\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"nomatch "') as mockio:
        CliBuilder(with_defaults=True).run()
        assert '--help\n' in mockio.output()


def cli_subcommands():
    return CliBuilder().has(
        subcommand('git').has(
            subcommand('push'),
            subcommand('remote').has(
                subcommand('set-url', 'rename'),
            ),
        ),
        subcommand('xrandr'),
    )


def test_autocomplete_base_command():
    with MockIO('--bash-autocomplete', 'app ') as mockio:
        cli_subcommands().run()
        assert 'git\n' in mockio.output()
        assert 'xrandr\n' in mockio.output()


def test_skip_nomatching_word():
    with MockIO('--bash-autocomplete', '"app nomatch "') as mockio:
        cli_subcommands().run()
        assert 'git\n' in mockio.output()
        assert 'xrandr\n' in mockio.output()


def test_autocomplete_subcommands():
    with MockIO('--bash-autocomplete', '"app g"') as mockio:
        cli_subcommands().run()
        assert mockio.output() == 'git\n'
    with MockIO('--bash-autocomplete', '"app git"') as mockio:
        cli_subcommands().run()
        assert mockio.output() == 'git\n'
    with MockIO('--bash-autocomplete', '"app git "') as mockio:
        cli_subcommands().run()
        assert 'push\n' in mockio.output()
        assert 'remote\n' in mockio.output()
        assert 'git\n' not in mockio.output()
        assert 'xrandr\n' not in mockio.output()
    with MockIO('--bash-autocomplete', '"app git r"') as mockio:
        cli_subcommands().run()
        assert 'remote\n' == mockio.output()
    with MockIO('--bash-autocomplete', '"app git remote"') as mockio:
        cli_subcommands().run()
        assert 'remote\n' == mockio.output()


def test_autocomplete_3rd_level_subcommand():
    with MockIO('--bash-autocomplete', '"app git remote "') as mockio:
        cli_subcommands().run()
        assert 'set-url\n' in mockio.output()
        assert 'remote\n' not in mockio.output()
        assert 'git\n' not in mockio.output()


def test_autocomplete_flags():
    def cli_flags():
        return CliBuilder().has(
            subcommand('sub').has(
                flag('--flag-local'),
            ),
            flag('--flag-global'),
        )
    with MockIO('--bash-autocomplete', 'app') as mockio:
        cli_flags().run()
        assert '--flag-global\n' in mockio.output()
        assert '--flag-local\n' not in mockio.output()
    with MockIO('--bash-autocomplete', 'app sub ') as mockio:
        cli_flags().run()
        assert '--flag-global\n' in mockio.output()
        assert '--flag-local\n' in mockio.output()


def test_autocomplete_parameters():
    def cli_parameters():
        return CliBuilder().has(
            subcommand('sub').has(
                parameter('--param-local'),
            ),
            parameter('--param-global'),
        )
    with MockIO('--bash-autocomplete', 'app') as mockio:
        cli_parameters().run()
        assert '--param-global\n' in mockio.output()
        assert '--param-local\n' not in mockio.output()
    with MockIO('--bash-autocomplete', 'app sub ') as mockio:
        cli_parameters().run()
        assert '--param-global\n' in mockio.output()
        assert '--param-local\n' in mockio.output()


def cli_parameters():
    return CliBuilder().has(
        subcommand('sub').has(
            parameter('--parameter', choices=list_screens),
        ),
    )


def test_autocomplete_parameter_name():
    with MockIO('--bash-autocomplete', '"app sub --param"') as mockio:
        cli_parameters().run()
        assert '--parameter\n' in mockio.output()
        assert '--parameter=\n' in mockio.output()


def test_autocomplete_parameters_choice_2params():
    with MockIO('--bash-autocomplete', '"app sub --parameter"') as mockio:
        cli_parameters().run()
        assert '--parameter\n' in mockio.output()
        assert '--parameter=\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"app sub --parameter "') as mockio:
        cli_parameters().run()
        assert 'HDMI\n' in mockio.output()
        assert 'eDP\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"app sub --parameter H"') as mockio:
        cli_parameters().run()
        assert mockio.output() == 'HDMI\n'


def test_autocomplete_parameters_choice_equal():
    with MockIO('--bash-autocomplete', '"app sub --parameter="') as mockio:
        cli_parameters().run()
        assert '--parameter=HDMI\n' not in mockio.output()
        assert 'HDMI\n' in mockio.output()
        assert 'eDP\n' in mockio.output()
    with MockIO('--bash-autocomplete', '"app sub --parameter=H"') as mockio:
        cli_parameters().run()
        assert mockio.output() == 'HDMI\n'


def test_autocomplete_pos_arguments_choice():
    def cli_argument():
        return CliBuilder().has(
            subcommand('sub').has(
                argument('pos', choices=['abc', 'def']),
            ),
        )
    with MockIO('--bash-autocomplete', '"app sub pos "') as mockio:
        cli_argument().run()
        assert 'abc\n' in mockio.output()
        assert 'def' in mockio.output()
    with MockIO('--bash-autocomplete', '"app sub pos a"') as mockio:
        cli_argument().run()
        assert 'abc\n' in mockio.output()
        assert 'def' not in mockio.output()


def test_autocomplete_command_last_word_space():
    with MockIO('--bash-autocomplete', 'app info age') as mockio:
        CliBuilder().has(
            subcommand('info').has(
                subcommand('age'),
            ),
        ).run()
        assert 'age\n' in mockio.output()


def test_doubled_proposals():
    with MockIO('--bash-autocomplete', 'app --version ') as mockio:
        CliBuilder(version='1').run()
        assert '-h\n' in mockio.output()
        assert '--help\n' in mockio.output()
        assert '--version\n' in mockio.output()
        assert '--bash-install\n' in mockio.output()
        assert '--bash-autocomplete\n' in mockio.output()
