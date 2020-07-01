from nuclear import *
from tests.asserts import MockIO
from tests.parser.actions import *


def test_run_default_single_action():
    with MockIO() as mockio:
        CliBuilder(run=print_ok).run()
        assert mockio.output() == 'ok\n'


def test_default_builder_action_with_redundant_args():
    with MockIO('push') as mockio:
        CliBuilder(run=print_ok, error_unrecognized=False).has(
            subcommand('commit', run=print_bad),
            subcommand('checkout', run=print_bad),
        ).run()
        assert 'ok\n' in mockio.output()
    with MockIO('push') as mockio:
        CliBuilder(error_unrecognized=False).has(
            subcommand('commit', run=print_bad),
            subcommand('checkout', run=print_bad),
            default_action(run=print_ok),
        ).run()
        assert 'ok\n' in mockio.output()
    with MockIO('push') as mockio:
        CliBuilder(run=print_bad, error_unrecognized=True).has(
            subcommand('commit', run=print_bad),
            subcommand('checkout', run=print_bad),
        ).run()
        assert 'bad' not in mockio.output()
        assert 'Syntax error: unrecognized arguments' in mockio.output()


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


def test_parent_default_action():
    with MockIO('nmcli', 'dev') as mockio:
        CliBuilder(run=print_ok).has(
            subcommand('nmcli').has(
                subcommand('dev')
            ),
        ).run()
        assert mockio.output() == 'ok\n'


def test_on_empty_action_overriden():
    with MockIO() as mockio:
        CliBuilder(run=print_bad, help_on_empty=True).has(
            flag('any')
        ).run()
        assert 'Usage' in mockio.output()
    with MockIO('--any') as mockio:
        CliBuilder(run=print_ok, help_on_empty=True).has(
            flag('any')
        ).run()
        assert mockio.output() == 'ok\n'
