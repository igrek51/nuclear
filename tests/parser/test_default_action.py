from cliglue import *
from tests.asserts import MockIO
from tests.parser.actions import *


def test_run_default_single_action():
    with MockIO() as mockio:
        CliBuilder(run=print_ok).run()
        assert mockio.output() == 'ok\n'


def test_default_builder_action_with_redundant_args():
    with MockIO('push') as mockio:
        CliBuilder(run=print_ok).has(
            subcommand('commit', run=print_bad),
            subcommand('checkout', run=print_bad),
        ).run()
        assert 'ok\n' in mockio.output()
    with MockIO('push') as mockio:
        CliBuilder().has(
            subcommand('commit', run=print_bad),
            subcommand('checkout', run=print_bad),
            default_action(run=print_ok),
        ).run()
        assert 'ok\n' in mockio.output()


def test_subcommand_default_action():
    with MockIO('git', 'push') as mockio:
        CliBuilder(run=print_bad).has(
            subcommand('nmcli').has(
                default_action(run=print_bad)
            ),
            subcommand('git', run=print_bad).has(
                subcommand('push').has(
                    default_action(run=print_ok)
                ),
            ),
        ).run()
        assert mockio.output() == 'ok\n'
