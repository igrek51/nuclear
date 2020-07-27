from nuclear.sublog import wrap_context, ContextError, log, logerr
from tests.asserts import MockIO


def test_sublog_wrapping():
    with MockIO() as mockio:
        with logerr():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    raise RuntimeError('dupa')

        with logerr():
            raise ContextError('dupa2', a=5, z='fifteen')

        with logerr():
            raise RuntimeError('dupa3')

        log.info('success', param='with_param')
        log.warn('attention')
        log.debug('trace')

        mockio.assert_match_uncolor('] initializing: liftoff: dupa '
                                    'request_id=42 speed=zero '
                                    'cause=RuntimeError traceback=(.*)/test_error_wrap.py:10$')
        mockio.assert_match_uncolor('] dupa2 a=5 z=fifteen '
                                    'cause=ContextError traceback=(.*)/test_error_wrap.py:13$')
        mockio.assert_match_uncolor('\\[ERROR] dupa3 '
                                    'cause=RuntimeError traceback=(.*)/test_error_wrap.py:16$')
        mockio.assert_match_uncolor('\\[INFO ] success param=with_param$')
        mockio.assert_match_uncolor('\\[WARN ] attention$')
        mockio.assert_match_uncolor('\\[DEBUG] trace$')


def test_sublog_traceback():
    with MockIO() as mockio:
        with logerr():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    disaster()

        mockio.assert_match_uncolor('ERROR] initializing: liftoff: disaster request_id=42 speed=zero '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_error_wrap.py:39,'
                                    '(.+)/test_error_wrap.py:49,'
                                    '(.+)/test_error_wrap.py:53$')


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
