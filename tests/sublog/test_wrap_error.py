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

        mockio.assert_match_uncolor('ERROR initializing: liftoff: dupa '
                                    'request_id=42 speed=zero '
                                    'cause=RuntimeError traceback=(.*)/test_wrap_error.py:10$')
        mockio.assert_match_uncolor('ERROR dupa2 a=5 z=fifteen '
                                    'cause=ContextError traceback=(.*)/test_wrap_error.py:13$')
        mockio.assert_match_uncolor('ERROR dupa3 '
                                    'cause=RuntimeError traceback=(.*)/test_wrap_error.py:16$')
        mockio.assert_match_uncolor('INFO  success param=with_param$')
        mockio.assert_match_uncolor('WARN  attention$')
        mockio.assert_match_uncolor('DEBUG trace$')
