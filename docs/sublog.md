# 📜 Sublog
**Sublog** is a *nuclear*'s contextual logging system that allows you to:
  
- display variables besides log messages: `logger.debug('message', airspeed=20)`,
- wrap errors with context: `with add_context('ignition')`,
- catch errors and show traceback in a concise, pretty format: `with error_handler()`.

```python
from nuclear.sublog import logger, error_handler, add_context

with error_handler():
    logger.debug('checking engine', temperature=85.0, pressure='12kPa')
    with add_context('ignition', request=42):
        logger.info('ignition ready', speed='zero')
        with add_context('liftoff'):
            raise RuntimeError('explosion')
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/img/sublog-demo.png?raw=true)

## Context logger
Use `nuclear.sublog.logger` to log message with a pretty format out of the box.

Pass additional context variables as keyword arguments to display them in the log message.

```python
from nuclear.sublog import logger

logger.info('info log')
logger.debug('debug log', var1=1, var2='two')
logger.info('not great not terrible', radioactivity=3.6)
logger.error('this is bad')
logger.exception(RuntimeError('this is worse'))
```

## Error handler
Use `nuclear.sublog.error_handler` to catch errors and show traceback in a concise, pretty format.

```python
from nuclear.sublog import error_handler

with error_handler():
    raise RuntimeError('explosion')
```

## Wrapping context
Use `nuclear.sublog.add_context` to wrap code with additional context information.
This will be included in in the log message, if an error occurs.

```python
from nuclear.sublog import add_context

with add_context('reloading plugins'):
    with add_context('loading config'):
        raise RuntimeError('file is missing')
```
This will produce an error with the following message:
```
reloading plugins: loading config: file is missing
```

Note that while each individual part of the message may not provide a comprehensive explanation of the error,
when combined, the whole message becomes highly informative.
This is the core principle behind enriching errors with context.
