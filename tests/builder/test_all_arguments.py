from typing import List

from cliglue.builder import *
from tests.testing_utils import MockIO


def print_all_args(remainder: List[str]):
    print(f'remainder: {", ".join(remainder)}')


def test_remaining_args():
    with MockIO('1', '2', '3') as mockio:
        CliBuilder(run=print_all_args).has(
            all_arguments('remainder'),
        ).run()
        assert mockio.output() == 'remainder: 1, 2, 3\n'


def test_remaining_args_empty():
    with MockIO() as mockio:
        CliBuilder(run=print_all_args).has(
            all_arguments('remainder'),
        ).run()
        assert mockio.output() == 'remainder: \n'


def test_pos_arg_with_remaining_args():
    def print_args(arg1, arg2, remainder: List[str]):
        print(f'args: {arg1} {arg2} {", ".join(remainder)}')

    with MockIO('1', '2', '3', '4') as mockio:
        CliBuilder(run=print_args).has(
            argument('arg1'),
            argument('arg2'),
            all_arguments('remainder'),
        ).run()
        assert mockio.output() == 'args: 1 2 3, 4\n'


def test_remaining_args_joined():
    def proint_remainder(remainder: str):
        print(f'remainder: {remainder}')

    with MockIO('1', '2', '3') as mockio:
        CliBuilder(run=proint_remainder).has(
            all_arguments('remainder', joined_with=' '),
        ).run()
        assert mockio.output() == 'remainder: 1 2 3\n'
