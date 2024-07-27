import os
from time import tzset
import time

from nuclear.sublog import logger, error_handler, init_logs
from tests.asserts import MockIO


def test_context_logger():
    for timezone in ['Europe/Warsaw', 'UTC']:
        _test_context_logger_tz(timezone)


def _test_context_logger_tz(timezone: str)
    os.environ['TZ'] = timezone
    tzset()
    tz_utc = time.timezone == 0  # in case timezone change didn't take effect
    init_logs()
    logger.debug('42')
    with MockIO() as mockio:
        with logger.contextualize(request_id=0xdeaddead) as logger2:
            logger2.debug('got request')
            with logger2.contextualize(user='igrek') as logger3:
                logger3.info('logged in', page='sweet home')
                logger.warn('im a root')

            logger2.debug('logged out')
        logger.debug('42')

        # datetime
        if tz_utc:
            mockio.assert_match('^\\[\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}Z\\] ')
        else:
            mockio.assert_match('^\\[\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\] ')
        # log level
        mockio.assert_match(' DEBUG ')
        # message with context
        mockio.assert_match(' got request, request_id=3735936685$')

        mockio.assert_match_uncolor('INFO  logged in, request_id=3735936685 user=igrek page="sweet home"$')
        mockio.assert_match_uncolor('WARN  im a root$')
        mockio.assert_match_uncolor('DEBUG logged out, request_id=3735936685$')
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

        mockio.assert_match_uncolor(' outside context, a=4$')
        mockio.assert_match_uncolor(' got request, request_id=3735936685$')
        mockio.assert_match_uncolor(' logged in, request_id=3735936685 user=igrek page=home$')
        mockio.assert_match_uncolor(' im a root, request_id=3735936685 user=igrek$')
        mockio.assert_match_uncolor(
            ' I\'m a pickle, cause=RuntimeError traceback=.+:52$')
        mockio.assert_match_uncolor(' logged out, request_id=3735936685$')
        mockio.assert_match_uncolor(' exited$')


def test_child_logger():
    with MockIO() as mockio:
        logger.warning('beware of Python loggers')
        mockio.assert_match_uncolor('] WARN  beware of Python loggers$')

    with MockIO() as mockio:
        logger.warning('beware of Python loggers')
        mockio.assert_match_uncolor('] WARN  beware of Python loggers$')


def test_hidden_log_time():
    try:
        init_logs(show_time=False)
        with MockIO() as mockio:
            logger.debug('logged in')
        mockio.assert_match('^DEBUG logged in$')
    finally:
        init_logs()
