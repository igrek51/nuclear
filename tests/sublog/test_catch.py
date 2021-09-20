from nuclear.sublog import wrap_context, logerr
from tests.asserts import MockIO


def test_sublog_traceback():
    with MockIO() as mockio:
        with logerr():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    disaster()

        mockio.assert_match_uncolor('ERROR] initializing: liftoff: disaster request_id=42 speed=zero '
                                    'cause=RuntimeError '
                                    'traceback="(.+)/test_catch.py:10, '
                                    '(.+)/test_catch.py:20, '
                                    '(.+)/test_catch.py:24"$')


def disaster():
    reason()


def reason():
    raise RuntimeError('disaster')


def test_keyboard_interrupt():
    with MockIO() as mockio:
        try:
            with logerr():
                raise KeyboardInterrupt()
            assert False, 'should exit'
        except SystemExit as e:
            assert str(e) == '1', 'should exit with error code 1'

        assert 'KeyboardInterrupt' in mockio.output()


def test_catch_with_context_name():
    with MockIO() as mockio:
        with logerr('hacking time'):
            raise RuntimeError('nope')

        mockio.assert_match_uncolor('ERROR] hacking time: nope '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_catch.py:42$')
