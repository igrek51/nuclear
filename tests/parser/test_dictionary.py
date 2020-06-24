from typing import Dict

from nuclear import *
from tests.asserts import MockIO, assert_cli_error


def test_dictionary_setting_value():
    def print_dict(config: Dict):
        print(config)

    with MockIO('--config', 'name', 'value') as mockio:
        CliBuilder(run=print_dict).has(
            dictionary('--config', '-c'),
        ).run()
        assert mockio.stripped() == "{'name': 'value'}"


def test_empty_dictionary():
    def print_dict(config: Dict):
        print(config)

    with MockIO() as mockio:
        CliBuilder(run=print_dict).has(
            dictionary('--config', '-c'),
        ).run()
        assert mockio.stripped() == "{}"


def test_setting_multiple_dict_values():
    def print_dict(config: Dict):
        print(config)

    with MockIO('--config', 'name1', '1', '-c', 'name2', '2') as mockio:
        CliBuilder(run=print_dict).has(
            dictionary('--config', '-c', value_type=int),
        ).run()
        assert mockio.stripped() == "{'name1': 1, 'name2': 2}"


def test_typed_dictionary():
    def print_dict(config: Dict):
        print(config)

    with MockIO('--config', '1', '2') as mockio:
        CliBuilder(run=print_dict).has(
            dictionary('--config', '-c', key_type=int, value_type=int),
        ).run()
        assert mockio.stripped() == "{1: 2}"


def test_explicit_var_name():
    def print_dict(configuration: Dict):
        print(configuration)

    with MockIO('-c', '1', '2') as mockio:
        CliBuilder(run=print_dict).has(
            dictionary('-c', name='configuration'),
        ).run()
        assert mockio.stripped() == "{'1': '2'}"


def test_incomplete_dict_params():
    with MockIO('-c'):
        cli = CliBuilder(reraise_error=True).has(
            dictionary('-c'),
        )
        assert_cli_error(lambda: cli.run(), 'missing key argument for dictionary')
    with MockIO('-c', 'name'):
        cli = CliBuilder(reraise_error=True).has(
            dictionary('-c'),
        )
        assert_cli_error(lambda: cli.run(), 'missing value argument for dictionary')
