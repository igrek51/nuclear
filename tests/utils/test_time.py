from cliglue.utils.time import *


def test_time_conversions():
    pattern = '%H:%M:%S, %d.%m.%Y'
    sample_date = '16:26:01, 20.12.2017'
    bad_date = '16:26:01 20.12.17dupa'
    dt = str2time(sample_date, pattern)
    assert dt is not None
    assert time2str(dt, pattern) == sample_date
    assert str2time(bad_date, pattern) is None
    assert time2str(None, pattern) is None
