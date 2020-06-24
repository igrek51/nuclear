import datetime

from nuclear import *
from nuclear.types.time import datetime_format, today_format
from tests.asserts import MockIO, assert_cli_error


def test_datetime_format_generator():
    def print_datetime(d):
        print(str(d))

    with MockIO('-d=2019-06-07') as mockio:
        CliBuilder(run=print_datetime).has(
            parameter('d', type=datetime_format('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')),
        ).run()
        assert mockio.stripped() == str(datetime.datetime(2019, 6, 7))


def test_today_format_generator():
    def print_datetime(d):
        print(str(d))

    with MockIO('-d=12:30') as mockio:
        CliBuilder(run=print_datetime).has(
            parameter('d', type=today_format('%H:%M:%S', '%H:%M')),
        ).run()
        now = datetime.datetime.now()
        assert mockio.stripped() == str(datetime.datetime(now.year, now.month, now.day, 12, 30, 0))


def test_invalid_datetime():
    def print_datetime(d):
        print(str(d))

    with MockIO('-d=2019'):
        cli = CliBuilder(run=print_datetime, usage_onerror=False, reraise_error=True).has(
            parameter('d', type=datetime_format('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')),
        )
        assert_cli_error(lambda: cli.run())
