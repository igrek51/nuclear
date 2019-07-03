from typing import List

from cliglue import *
from tests.asserts import MockIO


def print_all_args(remainder: List[str]):
    print(f'remainder: {", ".join(remainder)}')


def test_remaining_args():
    with MockIO('1', '2', '3') as mockio:
        CliBuilder(run=print_all_args).has(
            arguments('remainder'),
        ).run()
        assert mockio.output() == 'remainder: 1, 2, 3\n'


def test_remaining_args_empty():
    with MockIO() as mockio:
        CliBuilder(run=print_all_args).has(
            arguments('remainder'),
        ).run()
        assert mockio.output() == 'remainder: \n'


def test_pos_arg_with_remaining_args():
    def print_args(arg1, arg2, remainder: List[str]):
        print(f'args: {arg1} {arg2} {", ".join(remainder)}')

    with MockIO('1', '2', '3', '4') as mockio:
        CliBuilder(run=print_args).has(
            argument('arg1'),
            argument('arg2'),
            arguments('remainder'),
        ).run()
        assert mockio.output() == 'args: 1 2 3, 4\n'


def test_remaining_args_joined():
    def proint_remainder(remainder: str):
        print(f'remainder: {remainder}')

    with MockIO('1', '2', '3') as mockio:
        CliBuilder(run=proint_remainder).has(
            arguments('remainder', joined_with=' '),
        ).run()
        assert mockio.output() == 'remainder: 1 2 3\n'


def test_all_argument_in_lower_subcommand():
    def print_components(components):
        print(','.join(components))

    with MockIO('all', '1') as mockio:
        CliBuilder().has(
            subcommand('all', run=print_components),
            arguments('components'),
        ).run()
        assert mockio.output() == '1\n'
