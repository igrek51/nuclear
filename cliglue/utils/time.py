import datetime


def str2time(time_raw, pattern):
    """pattern: %Y-%m-%d, %H:%M:%S"""
    try:
        return datetime.datetime.strptime(time_raw, pattern)
    except ValueError as _:
        return None


def time2str(date_time, pattern):
    """pattern: %Y-%m-%d, %H:%M:%S"""
    if not date_time:
        return None
    return date_time.strftime(pattern)
