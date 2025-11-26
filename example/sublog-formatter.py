#!/usr/bin/env python3
import logging
import sys

from nuclear.sublog import logger, init_logs, RESET, STYLE_BRIGHT_RED, STYLE_YELLOW, STYLE_BLUE, STYLE_GREEN
from nuclear.utils.strings import strip_ansi_colors


def main():
    set_logging_formatter()
    logger.info('not great, not terrible', radioactivity=3.6)
    logger.error('this is bad')


def set_logging_formatter():
    init_logs()
    for handler in logging.getLogger().handlers:
        handler.setFormatter(SimpleFormatter())


class SimpleFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)
        self.plain_formatter = logging.Formatter(fmt='%(levelname)s %(message)s')

    log_level_templates = {
        'CRITICAL': f'{STYLE_BRIGHT_RED}CRIT {RESET}',
        'ERROR': f'{STYLE_BRIGHT_RED}ERROR{RESET}',
        'WARNING': f'{STYLE_YELLOW}WARN {RESET}',
        'INFO': f'{STYLE_BLUE}INFO {RESET}',
        'DEBUG': f'{STYLE_GREEN}DEBUG{RESET}',
    }

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname in self.log_level_templates:
            record.levelname = self.log_level_templates[record.levelname].format(record.levelname)
        line: str = self.plain_formatter.format(record)
        if not sys.stdout.isatty():
            line = strip_ansi_colors(line)
        return line


main()
