import os


def test_structured_logs():
    os.environ['STRUCTURED_LOGGING'] = 'true'
    from nuclear.sublog import logger, init_logs
    from tests.asserts import MockIO
    init_logs()
    try:
        with MockIO() as mockio:
            logger.debug('checking engine', temperature=85.0, pressure='12kPa')
            mockio.assert_match('^{}$')
    finally:
        del os.environ['STRUCTURED_LOGGING']
