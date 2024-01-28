from nuclear.sublog import add_context, ContextError, log, error_handler, exception_details
from tests.asserts import MockIO


def test_sublog_wrapping():
    with MockIO() as mockio:
        with error_handler():
            with add_context('initializing', request_id=42):
                with add_context('liftoff', speed='zero'):
                    raise RuntimeError('dupa')

        with error_handler():
            raise ContextError('dupa2', a=5, z='fifteen')

        with error_handler():
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
        with add_context('initializing', request_id=42):
            with add_context('liftoff', speed='zero'):
                try:
                    raise ValueError('dupa')
                except ValueError as e:
                    raise RuntimeError('parent') from e
    except Exception as e:
        assert str(e) == 'initializing: liftoff: parent: dupa'
        assert exception_details(e).startswith('initializing: liftoff: parent: dupa, cause=ValueError, traceback=')


    try:
        with add_context('initializing'):
            try:
                raise ValueError('nothing inside')
            except ValueError as e:
                raise ContextError('wrapper') from e
    except Exception as e:
        assert str(e) == 'initializing: wrapper: nothing inside'
