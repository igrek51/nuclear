from datetime import datetime, timezone

PARSE_DATE_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
]


def now() -> datetime:
    """Return current datetime with UTC timezone set"""
    return datetime.now(timezone.utc)


def now_tz() -> datetime:
    """Return current datetime with local timezone set"""
    return datetime.now().astimezone()


def now_timestamp() -> int:
    return datetime_to_timestamp(now())


def datetime_to_timestamp(dt: datetime) -> int:
    """Convert datetime.datetime to integer timestamp in seconds"""
    return int(dt.timestamp())


def timestamp_to_datetime(timestamp: int) -> datetime:
    """Convert integer timestamp in seconds to datetime.datetime"""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def datetime_to_str(dt: datetime) -> str:
    """Convert datetime to ISO 8601 format"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


def date_to_str(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d')


def str_iso8601_to_datetime(text: str) -> datetime:
    return datetime.strptime(text, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def parse_date(text: str) -> datetime:
    for date_format in PARSE_DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    raise ValueError(f'cannot parse {text} as date')


def str_to_timestamp_ms(text: str) -> int:
    dt = parse_date(text)
    return int(dt.timestamp() * 1000)


def timestamp_pretty_ago(timestamp: int) -> str:
    """
    Convert past date to user-friendly description compared to current datetime.
    eg.: 'an hour ago', 'yesterday', '3 months ago', 'just now'
    """
    diff = now() - timestamp_to_datetime(timestamp)
    second_diff: int = diff.seconds
    day_diff: int = diff.days

    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return f"{second_diff} seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return f"{second_diff // 60} minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return f"{second_diff // 3600} hours ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return f"{day_diff} days ago"
    if day_diff // 7 == 1:
        return f"a week ago"
    if day_diff < 31:
        return f"{day_diff // 7} weeks ago"
    if day_diff // 30 == 1:
        return f"a month ago"
    if day_diff < 365:
        return f"{day_diff // 30} months ago"
    if day_diff // 365 == 1:
        return f"a year ago"
    return f"{day_diff // 365} years ago"
