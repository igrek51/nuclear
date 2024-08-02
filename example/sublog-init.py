from nuclear.sublog import logger, init_logs


init_logs(show_time=False, show_log_level=False)

logger.debug('checking engine', temperature=85.0, pressure='12kPa')
logger.info('ignition ready', speed='zero')
logger.warning('Attention')
