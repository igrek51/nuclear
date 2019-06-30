from cliglue import *
from tests.asserts import MockIO, assert_cli_error


def print_pos_arg1(arg1):
    print(f'arg1: {arg1}')


def print_2_args(arg1, arg2):
    print(f'args: {arg1}, {arg2}')


def test_1_positional_arg():
    with MockIO('val') as mockio:
        CliBuilder(run=print_pos_arg1).has(
            argument('arg1'),
        ).run()
        assert mockio.output() == 'arg1: val\n'


def test_2_positional_args():
    with MockIO('val1', 'val2') as mockio:
        CliBuilder(run=print_2_args).has(
            argument('arg1'),
            argument('arg2'),
        ).run()
        assert mockio.output() == 'args: val1, val2\n'
    with MockIO('val1', 'val2') as mockio:
        CliBuilder(run=print_2_args).has(
            argument('arg2'),
            argument('arg1'),
        ).run()
        assert mockio.output() == 'args: val2, val1\n'


def test_optional_argument():
    with MockIO() as mockio:
        CliBuilder(run=print_pos_arg1).has(
            argument('arg1', required=False),
        ).run()
        assert mockio.output() == 'arg1: None\n'


def test_missing_required_argument():
    with MockIO():
        cli = CliBuilder(run=print_pos_arg1, help_onerror=False, reraise_error=True).has(
            argument('arg1'),
        )
        assert_cli_error(lambda: cli.run())
