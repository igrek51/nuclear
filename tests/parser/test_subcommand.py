from cliglue import *
from tests.asserts import MockIO
from tests.parser.actions import *


def test_run_selected_command():
    with MockIO('push') as mockio:
        CliBuilder().has(
            subcommand('commit', run=print_bad),
            subcommand('push', run=print_ok),
            subcommand('checkout', run=print_bad),
        ).run()
        assert mockio.output() == 'ok\n'


def test_2nd_level_subcommand():
    with MockIO('git', 'remote') as mockio:
        CliBuilder().has(
            subcommand('git', run=print_bad).has(
                subcommand('remote', run=print_ok),
            ),
        ).run()
        assert mockio.output() == 'ok\n'


def test_run_selected_subcommand():
    with MockIO('git', 'remote', 'set-url') as mockio:
        CliBuilder().has(
            subcommand('git', run=print_bad).has(
                subcommand('push', run=print_bad),
                subcommand('remote', run=print_bad).has(
                    subcommand('add', run=print_bad),
                    subcommand('set-url', run=print_ok),
                ),
            ),
            subcommand('nmcli', run=print_bad),
        ).run()
        assert mockio.output() == 'ok\n'
