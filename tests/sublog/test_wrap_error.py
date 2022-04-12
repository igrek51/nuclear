from nuclear.sublog import wrap_context, ContextError, log, logerr, short_exception_details
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


def test_sublog_wrapping_try_string():
    try:
        with wrap_context('initializing', request_id=42):
            with wrap_context('liftoff', speed='zero'):
                try:
                    raise ValueError('dupa')
                except ValueError as e:
                    raise RuntimeError('parent') from e
    except Exception as e:
        assert str(e) == 'initializing: liftoff: parent: dupa'
        assert short_exception_details(e).startswith('initializing: liftoff: parent: dupa, cause=ValueError, traceback=')


    try:
        with wrap_context('initializing'):
            try:
                raise ValueError('nothing inside')
            except ValueError as e:
                raise ContextError('wrapper') from e
    except Exception as e:
        assert str(e) == 'initializing: wrapper: nothing inside'
