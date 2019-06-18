from cliglue.utils.strings import *
from tests.asserts import assert_error


def test_split_lines():
    assert nonempty_lines('a\nb\nc') == ['a', 'b', 'c']
    assert nonempty_lines('\na\n\n') == ['a']
    assert nonempty_lines('\n\n\n') == []
    assert nonempty_lines('') == []
    assert nonempty_lines('a\n\n\r\nb') == ['a', 'b']


def test_split_to_tuple():
    assert split_to_tuple('a', 1) == ('a',)
    assert split_to_tuple('', 1) == ('',)
    assert_error(lambda: split_to_tuple('a', 2))
    assert split_to_tuple('a\tb', 2) == ('a', 'b')
    assert_error(lambda: split_to_tuple('a\tb', 1))
    assert_error(lambda: split_to_tuple('a\tb\t', 2))
    assert split_to_tuple('a\tb\t', 3) == ('a', 'b', '')
    assert split_to_tuple('a\tb\tc', 3) == ('a', 'b', 'c')
    assert split_to_tuple('a b c', 3, ' ') == ('a', 'b', 'c')
    # no attrsCount verification
    assert split_to_tuple('a b c', splitter=' ') == ('a', 'b', 'c')
    assert split_to_tuple('a') == ('a',)


def test_split_to_tuples():
    assert split_to_tuples('a\tb\tc\nd\te\tf', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('\n\na\tb\tc\n\nd\te\tf\n', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('a\tb\tc', 3) == [('a', 'b', 'c')]
    # splitted list as input
    assert split_to_tuples(['a\tb\tc', 'd\te\tf'], 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples(['a\tb\tc'], 3) == [('a', 'b', 'c')]
