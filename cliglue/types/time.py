from datetime import datetime, date, time
from typing import Callable

from cliglue.parser.error import CliSyntaxError


def datetime_format(*formats: str) -> Callable[[str], datetime]:
    """format: %Y-%m-%d %H:%M:%S"""

    def parser(arg: str):
        return _parse_date_formats(arg, *formats)

    return parser


def today_format(*formats: str) -> Callable[[str], datetime]:
    def parser(arg: str):
        today: date = datetime.now().date()
        parsed_time: time = _parse_date_formats(arg, *formats).time()
        return datetime.combine(today, parsed_time)

    return parser


iso_date: Callable[[str], datetime] = datetime_format('%Y-%m-%d')
iso_time: Callable[[str], datetime] = datetime_format('%H:%M:%S')
iso_datetime: Callable[[str], datetime] = datetime_format('%Y-%m-%d %H:%M:%S')


def _parse_date_formats(s: str, *formats: str) -> datetime:
    for time_format in formats:
        try:
            return _parse_date(s, time_format)
        except ValueError:
            pass
    raise CliSyntaxError('invalid datetime format: ' + s)


def _parse_date(s: str, time_format: str):
    return datetime.strptime(s, time_format)
