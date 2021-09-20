## Logging with sublog
`sublog` is a logging system that allows you to:  
- display variables besides log messages: `log.debug('message', airspeed=20)`,
- wrap errors with context: `with wrap_context('ignition')`,
- catch errors and show traceback in a concise, pretty format: `with  logerr()`.

```python
from nuclear.sublog import log, logerr, wrap_context

with logerr():
    log.debug('checking engine', temperature=85.0, pressure='12kPa')
    with wrap_context('ignition', request=42):
        log.info('ignition ready', speed='zero')
        with wrap_context('liftoff'):
            raise RuntimeError('explosion')
```

![sublog demo](https://github.com/igrek51/nuclear/blob/master/docs/img/sublog-demo.png?raw=true)

