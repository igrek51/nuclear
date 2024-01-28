from nuclear.utils.time import datetime_to_str, parse_date


def test_time_conversions():
    sample_date = '16:26:01T2017-12-20+0000'
    dt = parse_date(sample_date)
    assert dt is not None
    assert datetime_to_str(dt) == sample_date
