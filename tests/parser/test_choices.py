from nuclear import parameter
from nuclear.parser.value import generate_value_choices


def test_generate_choices_from_list():
    assert generate_value_choices(parameter('key', choices=[])) == []
    assert generate_value_choices(parameter('key', choices=['abc'])) == ['abc']
    assert generate_value_choices(parameter('key', choices=['1', '2', '3'])) == ['1', '2', '3']


def test_generate_choices_from_set():
    assert generate_value_choices(parameter('key', choices=set())) == []
    assert generate_value_choices(parameter('key', choices={'abc'})) == ['abc']


def test_generate_choices_from_tuple():
    assert generate_value_choices(parameter('key', choices=())) == []
    assert generate_value_choices(parameter('key', choices=('abc',))) == ['abc']
    assert generate_value_choices(parameter('key', choices=('1', '2', '3'))) == ['1', '2', '3']


def test_generate_choices_from_dicts():
    items = {'a': '1'}
    assert generate_value_choices(parameter('key', choices=items.keys())) == ['a']
    assert generate_value_choices(parameter('key', choices=items.values())) == ['1']


def test_generate_choices_from_callable():
    def provide():
        return ['val', '2']

    assert generate_value_choices(parameter('key', choices=provide)) == ['val', '2']
