from nuclear.args.args_que import ArgsQue


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


def test_removing_inside_loop():
    args = ArgsQue(['1', '2', '3', '4'])
    result = []
    for arg in args:
        args.pop_current()
        args.pop_current()
        result += arg
    assert result == ['1', '3']
    assert not args
    assert len(args) == 0


def test_removing_by_3():
    args = ArgsQue(['1', '2', '3', '4', '5', '6'])
    result = []
    for _ in args:
        for _ in range(2):
            part = []
            for _ in range(3):
                part.append(args.pop_current())
            result.append(part)

    assert result == [['1', '2', '3'], ['4', '5', '6']]
    assert not args
    assert len(args) == 0


def test_just_peeking():
    args = ArgsQue(['1', '2'])
    result = []
    for _ in args:
        result.append(args.peek_current())
        result.append(args.pop_current())

    assert args.peek_current() is None
    assert result == ['1', '1', '2', '2']


def test_pop_all():
    args = ArgsQue(['1', '2'])
    assert args.pop_all() == ['1', '2']
    assert args.pop_all() == []
