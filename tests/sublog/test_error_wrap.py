from nuclear.sublog import wrap_context, log_error, ContextError, log
from tests.asserts import MockIO


def test_sublog_wrapping():
    with MockIO() as mockio:
        with log_error():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    raise RuntimeError('dupa')

        with log_error():
            raise ContextError('dupa2', a=5, z='fifteen')

        with log_error():
            raise ContextError('dupa3')

        log.info('success', param='with_param')
        log.warn('attention')
        log.debug('trace')

        mockio.assert_match_uncolor('] initializing: liftoff: dupa '
                                    'request_id=42 speed=zero '
                                    'traceback=(.*)/test_error_wrap.py:10$')
        mockio.assert_match_uncolor('] dupa2 a=5 z=fifteen '
                                    'traceback=(.*)/test_error_wrap.py:13$')
        mockio.assert_match_uncolor('\\[ERROR] dupa3 '
                                    'traceback=(.*)/test_error_wrap.py:16$')
        mockio.assert_match_uncolor('\\[INFO ] success param=with_param$')
        mockio.assert_match_uncolor('\\[WARN ] attention$')
        mockio.assert_match_uncolor('\\[DEBUG] trace$')


def test_sublog_traceback():
    with MockIO() as mockio:
        with log_error():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    disaster()

        mockio.assert_match_uncolor('ERROR] initializing: liftoff: disaster request_id=42 speed=zero '
                                    'traceback=(.+)/test_error_wrap.py:39,'
                                    '(.+)/test_error_wrap.py:48,'
                                    '(.+)/test_error_wrap.py:52$')


def disaster():
    reason()


def reason():
    raise RuntimeError('disaster')


def test_keyboard_interrupt():
    with MockIO() as mockio:
        try:
            with log_error():
                raise KeyboardInterrupt()
            assert False, 'should exit'
        except SystemExit as e:
            assert str(e) == '1', 'should exit with error code 1'

        assert 'KeyboardInterrupt' in mockio.output()
