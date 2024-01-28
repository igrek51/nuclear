from nuclear.sublog import logger, error_handler
from tests.asserts import MockIO


def test_context_logger():
    with MockIO() as mockio:
        with logger.contextualize(request_id=0xdeaddead) as logger2:
            logger2.debug('got request')
            with logger2.contextualize(user='igrek') as logger3:
                logger3.info('logged in', page='sweet home')
                logger.warn('im a root')

            logger2.debug('logged out')
        logger.debug(42)

        # datetime
        mockio.assert_match('^\x1b\\[2m\\[\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\]\x1b\\[0m ')
        # log level
        mockio.assert_match(' \x1b\\[32mDEBUG\x1b\\[0m ')
        # message with context
        mockio.assert_match(' got request \x1b\\[32mrequest_id=\x1b\\[1m3735936685\x1b\\[0m$')

        mockio.assert_match_uncolor('INFO  logged in request_id=3735936685 user=igrek page="sweet home"$')
        mockio.assert_match_uncolor('WARN  im a root$')
        mockio.assert_match_uncolor('DEBUG logged out request_id=3735936685$')
        mockio.assert_match_uncolor('DEBUG 42$')


def test_root_context_logger():
    with MockIO() as mockio:
        logger.debug('outside context', a=4)

        with logger.contextualize(request_id=0xdeaddead) as context_logger:
            context_logger.debug('got request')

            with context_logger.contextualize(user='igrek') as logger3:
                logger3.info('logged in', page='home')
                with error_handler():
                    logger3.warning('im a root')
                    raise RuntimeError("I'm a pickle")

            context_logger.debug('logged out')

        logger.debug('exited')

        mockio.assert_match_uncolor(' outside context a=4$')
        mockio.assert_match_uncolor(' got request request_id=3735936685$')
        mockio.assert_match_uncolor(' logged in request_id=3735936685 user=igrek page=home$')
        mockio.assert_match_uncolor(' im a root request_id=3735936685 user=igrek$')
        mockio.assert_match_uncolor(
            ' I\'m a pickle request_id=3735936685 user=igrek cause=RuntimeError traceback=.+:40$')
        mockio.assert_match_uncolor(' logged out request_id=3735936685$')
        mockio.assert_match_uncolor(' exited$')


def test_child_logger():
    with MockIO() as mockio:
        logger.warning('beware of Python loggers')
        mockio.assert_match_uncolor('] WARN  beware of Python loggers$')

    with MockIO() as mockio:
        logger.warning('beware of Python loggers')
        mockio.assert_match_uncolor('] WARN  beware of Python loggers$')
