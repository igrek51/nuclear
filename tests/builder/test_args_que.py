from cliglue.args.args_que import ArgsQue


def test_iterating_all():
    args = ArgsQue(['1', '2', '3'])
    assert args
    assert len(args) == 3
    result = []
    for arg in args:
        result += arg
    assert result == ['1', '2', '3']
    # test iterating 2nd time
    result = []
    for arg in args:
        result += arg
    assert result == ['1', '2', '3']


def test_removing_while_iterating():
    args = ArgsQue(['1', '2', '3'])
    result = []
    for arg in args:
        result += arg
        if arg == '2':
            args.pop_current()
    assert result == ['1', '2', '3']
    result = []
    for arg in args:
        result += arg
    assert result == ['1', '3']


def test_removing_all():
    args = ArgsQue(['1', '2', '3'])
    result = []
    for arg in args:
        result += arg
        args.pop_current()
    assert result == ['1', '2', '3']
    assert not args
    assert len(args) == 0
