#!/usr/bin/env python3
from nuclear.sublog import log, logerr, wrap_context

with logerr():
    log.debug('checking engine', temperature=85.0, pressure='12kPa')
    with wrap_context('ignition', request=42):
        log.info('ignition ready', speed='zero')
        with wrap_context('liftoff'):
            raise RuntimeError('explosion')
