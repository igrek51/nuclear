from typing import List

from nuclear import *
from tests.asserts import MockIO, assert_cli_error


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


def test_exact_many_arguments_count():
    with MockIO('all', '2') as mockio:
        CliBuilder(reraise_error=True, run=lambda components: print(len(components))).has(
            arguments('components', count=2),
        ).run()
        assert mockio.stripped() == '2'
    with MockIO():
        cli = CliBuilder(reraise_error=True).has(
            arguments('components', count=2),
        )
        assert_cli_error(lambda: cli.run())


def test_exact_many_arguments_count_and_superfluous():
    with MockIO('all', '2', '3') as mockio:
        CliBuilder(reraise_error=True, error_unrecognized=False, run=lambda components: print(components)).has(
            arguments('components', count=2),
        ).run()
        assert "['all', '2']" in mockio.stripped()


def test_min_many_arguments_count_syntax_error():
    with MockIO():
        cli = CliBuilder(reraise_error=True).has(
            arguments('components', min_count=1),
        )
        assert_cli_error(lambda: cli.run())


def test_min_many_arguments_count():
    with MockIO('one'):
        CliBuilder(reraise_error=True).has(
            arguments('components', min_count=1),
        ).run()


def test_max_many_arguments_count():
    with MockIO('one', 'two') as mockio:
        CliBuilder(reraise_error=True, error_unrecognized=False, run=lambda words: print(len(words))).has(
            arguments('words', max_count=1),
        ).run()
        assert '1' in mockio.stripped()
    with MockIO('one') as mockio:
        CliBuilder(reraise_error=True, run=lambda words: print(len(words))).has(
            arguments('words', max_count=1),
        ).run()
        assert '1' in mockio.stripped()


def test_parsing_many_arguments_typed():
    with MockIO('1', '41') as mockio:
        CliBuilder(run=lambda numbers: print(sum(numbers))).has(
            arguments('numbers', type=int),
        ).run()
        assert mockio.stripped() == '42'


def test_multiple_many_arguments_rules():
    with MockIO('1', '41', 'abc') as mockio:
        CliBuilder(run=lambda numbers, letters: print(letters + numbers)).has(
            arguments('numbers', count=2),
            arguments('letters'),
        ).run()
        assert mockio.stripped() == "['abc', '1', '41']"


def test_strict_choices():
    with MockIO('4'):
        cli = CliBuilder(reraise_error=True).has(
            arguments('a', choices=['42'], strict_choices=True),
        )
        assert_cli_error(lambda: cli.run())

    with MockIO('42'):
        CliBuilder(reraise_error=True).has(
            arguments('a', choices=['42'], strict_choices=True),
        ).run()

    def complete():
        return ['42']

    with MockIO('42'):
        CliBuilder(reraise_error=True).has(
            arguments('a', choices=complete, strict_choices=True),
        ).run()


def test_parsing_syntax_error():
    with MockIO('notanumber'):
        cli = CliBuilder(reraise_error=True).has(
            arguments('nums', type=int),
        )
        assert_cli_error(lambda: cli.run(), 'parsing many arguments "nums":')
