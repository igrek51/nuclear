from nuclear.sublog import add_context, ContextError, logger, error_handler, exception_details, init_logs
from tests.asserts import MockIO


def test_sublog_wrapping():
    init_logs()
    with MockIO() as mockio:
        with error_handler():
            with add_context('initializing', request_id=42):
                with add_context('liftoff', speed='zero'):
                    raise RuntimeError('dupa')

        with error_handler():
            raise ContextError('dupa2', a=5, z='fifteen')

        with error_handler():
            raise RuntimeError('dupa3')

        logger.info('success', param='with_param')
        logger.warn('attention')
        logger.debug('trace')

        mockio.assert_match_uncolor('ERROR initializing: liftoff: dupa, '
                                    'request_id=42 speed=zero '
                                    'cause=RuntimeError traceback=(.*)/test_wrap_error.py:11$')
        mockio.assert_match_uncolor('ERROR dupa2, a=5 z=fifteen '
                                    'cause=ContextError traceback=(.*)/test_wrap_error.py:14$')
        mockio.assert_match_uncolor('ERROR dupa3, '
                                    'cause=RuntimeError traceback=(.*)/test_wrap_error.py:17$')
        mockio.assert_match_uncolor('INFO  success, param=with_param$')
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
        assert exception_details(e).startswith('initializing: liftoff: parent: dupa, cause=ValueError, traceback='), exception_details(e)


    try:
        with add_context('initializing'):
            try:
                raise ValueError('nothing inside')
            except ValueError as e:
                raise ContextError('wrapper') from e
    except Exception as e:
        assert str(e) == 'initializing: wrapper: nothing inside'
