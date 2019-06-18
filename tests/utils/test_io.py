import sys

from cliglue.utils.input import input_required
from cliglue.utils.output import debug, info, warn, error, fatal
from tests.asserts import MockIO, assert_error


def test_output():
    with MockIO() as mockio:
        debug('message')
        assert mockio.output_contains('message')
        assert mockio.output_contains('debug')
        info('message')
        assert mockio.output_contains('info')
        warn('message')
        assert mockio.output_contains('warn')
        error('message')
        assert mockio.output_contains('ERROR')
        info(7)
        assert mockio.output_contains('7')


def test_input_required():
    sys.stdin = open('tests/utils/res/inputRequired')
    assert input_required('required: ') == 'valid'


def test_fatal():
    assert_error(lambda: fatal('fatality'))
    assert_error(lambda: fatal('fatality'), 'fatality')
