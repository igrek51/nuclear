from nuclear import *
from tests.asserts import MockIO
from tests.parser.actions import *


def test_error_on_unrecognized_arg():
    with MockIO('noway', '--noarg') as mockio:
        CliBuilder(run=print_bad, error_unrecognized=True).has(
            subcommand('noway', run=print_bad),
        ).run()
        assert 'bad' not in mockio.output()
        assert 'unrecognized arguments: --noarg\n' in mockio.output()


def test_unrecognized_arg_before_subcommand():
    with MockIO('--noarg', 'noway') as mockio:
        CliBuilder(run=print_bad, error_unrecognized=True).has(
            subcommand('noway', run=print_bad),
        ).run()
        assert 'bad' not in mockio.output()
        assert 'unrecognized arguments: --noarg noway\n' in mockio.output()


def test_ignore_unrecognized_args():
    with MockIO('--noarg', 'noway') as mockio:
        CliBuilder(run=print_ok, error_unrecognized=False).run()
        assert 'ok' in mockio.output()
        assert 'unrecognized arguments: --noarg noway\n' in mockio.output()
