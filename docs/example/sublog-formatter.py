#!/usr/bin/env python3
from nuclear.sublog import logger, init_logs


init_logs()

logger.info('not great, not terrible', radioactivity=3.6)
logger.error('this is bad')
