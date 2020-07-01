import sys

from nuclear.utils.input import input_required


def test_input_required():
    sys.stdin = open('tests/utils/res/inputRequired')
    assert input_required('required: ') == 'valid'
