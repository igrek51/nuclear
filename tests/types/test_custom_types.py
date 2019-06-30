import datetime

from cliglue import *
from cliglue.types.filesystem import existing_file
from cliglue.types.time import datetime_format
from tests.asserts import MockIO, assert_cli_error


def test_custom_parser():
    def my_parser(arg):
        return eval(arg)

    def print_my(my):
        print(my)

    with MockIO('--my=17+5') as mockio:
        CliBuilder(run=print_my).has(
            parameter('my', type=my_parser),
        ).run()
        assert mockio.stripped_output() == '22'


def test_datetime_arg():
    def print_datetime(d):
        print(str(d))

    with MockIO('-d=2019-06-07') as mockio:
        CliBuilder(run=print_datetime).has(
            parameter('d', type=datetime_format('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')),
        ).run()
        assert mockio.stripped_output() == str(datetime.datetime(2019, 6, 7))


def test_invalid_datetime():
    def print_datetime(d):
        print(str(d))

    with MockIO('-d=2019'):
        cli = CliBuilder(run=print_datetime, help_onerror=False, reraise_error=True).has(
            parameter('d', type=datetime_format('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')),
        )
        assert_cli_error(lambda: cli.run())


def test_invalid_file():
    def print_file(file):
        print(file)

    with MockIO('--file=dupa'):
        cli = CliBuilder(run=print_file, help_onerror=False, reraise_error=True).has(
            parameter('file', type=existing_file),
        )
        assert_cli_error(lambda: cli.run())
