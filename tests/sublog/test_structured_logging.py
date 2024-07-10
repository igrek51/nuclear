import os

from nuclear.sublog import logger, init_logs
from tests.asserts import MockIO


def test_structured_logs():
    os.environ['NUCLEAR_STRUCTURED_LOGGING'] = 'true'
    logger.structured_logging = True
    init_logs()
    try:
        with MockIO() as mockio:
            logger.debug('checking engine', temperature=85.0, pressure='12kPa')
            mockio.assert_match(r'^{"time": ".+-.+-.+T.+:.+:.+\..+Z", "level": "DEBUG", "message": "checking engine", "temperature": 85.0, "pressure": "12kPa"}$')
    finally:
        del os.environ['NUCLEAR_STRUCTURED_LOGGING']
        logger.structured_logging = False
