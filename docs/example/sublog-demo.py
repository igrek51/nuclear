#!/usr/bin/env python3
from nuclear.sublog import logger, error_handler, add_context, get_logger

with error_handler():
    logger.debug('checking engine', temperature=85.0, pressure='12kPa')
    with add_context('ignition', request=42):
        logger.info('ignition ready', speed='zero')
        with add_context('liftoff'):
            raise RuntimeError('explosion')

logger = get_logger(__name__)
logger.warning('Python logger works too')
