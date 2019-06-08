from datetime import datetime, date, time
from typing import Callable

from cliglue.parser.error import ArgumentSyntaxError


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


def _parse_date_formats(s: str, *formats: str) -> datetime:
    for time_format in formats:
        try:
            return _parse_date(s, time_format)
        except ValueError:
            pass
    raise ArgumentSyntaxError('invalid datetime format: ' + s)


def _parse_date(s: str, time_format: str):
    return datetime.strptime(s, time_format)
