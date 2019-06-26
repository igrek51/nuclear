import sys

from cliglue.utils.input import input_required
from cliglue.utils.output import debug, info, warn, error, fatal
from tests.asserts import MockIO, assert_error


def test_output():
    with MockIO() as mockio:
        debug('message')
        assert 'message' in mockio.output()
        assert 'debug' in mockio.output()
        info('message')
        assert 'info' in mockio.output()
        warn('message')
        assert 'warn' in mockio.output()
        error('message')
        assert 'ERROR' in mockio.output()
        info(7)
        assert '7' in mockio.output()


def test_input_required():
    sys.stdin = open('tests/utils/res/inputRequired')
    assert input_required('required: ') == 'valid'


def test_fatal():
    assert_error(lambda: fatal('fatality'))
    assert_error(lambda: fatal('fatality'), expected_msg='fatality')
