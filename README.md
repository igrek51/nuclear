# ☢️ Nuclear
[![GitHub version (latest SemVer)](https://img.shields.io/github/v/tag/igrek51/nuclear?label=github&sort=semver)](https://github.com/igrek51/nuclear)
[![PyPI](https://img.shields.io/pypi/v/nuclear)](https://pypi.org/project/nuclear)
[![Github Pages](https://img.shields.io/badge/docs-github.io-blue)](https://igrek51.github.io/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/igrek51/nuclear/test.yml?branch=master&label=tests)](https://github.com/igrek51/nuclear/actions?query=workflow%3Atest)

<div align="center">
    <a href="https://github.com/igrek51/nuclear">GitHub</a>
    -
    <a href="https://pypi.org/project/nuclear">PyPI</a>
    -
    <a href="https://igrek51.github.io/nuclear">Documentation</a>
</div>

*Nuclear* is a binding glue for CLI applications.
It consists of tools for building CLI applications in Python, including:

- [CLI parser](https://igrek51.github.io/nuclear/quick-start/) for building nested CLI commands
- [Sublog](https://igrek51.github.io/nuclear/sublog/) - contextual logger
- [WAT](https://igrek51.github.io/nuclear/inspect/) - inspection tool
- [Shell utilities](https://igrek51.github.io/nuclear/shell/)


# CLI Demo
```python
from nuclear import CliBuilder

cli = CliBuilder()

@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """
    Say hello
    :param decode: Decode name as base64
    """
    message = f"I'm a {b64decode(name).decode() if decode else name}!"
    print(' '.join([message] * repeat))

@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

@cli.add_command('calculate', 'primes')
def calculate_primes(n: int):
    """List prime numbers using Sieve of Eratosthenes"""
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), range(2, n), set(range(2, n)))))

cli.run()
```

![](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-live.gif?raw=true)

See [demo.py](https://github.com/igrek51/nuclear/blob/master/docs/demo/demo-decorator.py) for a complete example.

# Installation
```bash
python3 -m pip install --upgrade nuclear
```

You need Python 3.8 or newer.


# 🙀 WAT Inspector

**Nuclear** comes with a powerful inspection tool
that allows you to delve into and examine unknown objects at runtime.

> "Wat" is a variant of the English word "what" that is often used to express confusion or disgust

If you find yourself deep within the Python console, feeling dazed and confused,
wondering "WAT? What's that thing?",
that's where the `wat` inspector comes in handy.

Start the Python Interpreter (or attach to your program) and execute `wat(object)` on any `object`
to investigate its
**type**, **formatted value**, **variables**, **methods**, **parent types**, **signature**,
**documentation**, and even its **source code**.

<video width="100%" controls="true" allowfullscreen="true" src="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect.mp4" poster="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect-poster.png">
</video>

## Import
Import inspection tools from **nuclear** package.
```sh
pip install nuclear
```
```python
from nuclear import wat
```

Alternatively, use **Insta-Load** in the section below.

### Insta-Load
If you want to debug something quickly,
you don't even need to install **nuclear** package to use `wat` inspector.

Load it on the fly by pasting this snippet to your Python interpreter:
```python
import base64, zlib
code = 'eJzNWutu20YW/u+nGLg/RMWMajd7AdQqu2njTQOk7SJ1twhsg6BEyuaGIgWSSuJqBfQh9hn2wfZJ9lzmcoYXyfb2RwPEkmbO+ebc5syZy7IqVyqJm3iRx3Wd1ipbrcuqcU1HuiEr6nW6aFRcq7pJIv3T9JaWrkrNt/quPloifHO3zoobg/yiuAvVy2zRhOpNVsPfH9ZNVhZxHqqLu3UaqtdNWsXzHL79VEDH0V+dLPRXveaxvymLZXYzPVLwr74F6Kmal2VOv5NNkaSVaCjKpFzUoiEvixvxc1Emqf45NN6Lpqmy+aZJecgiXgFH3VT060Ocb+AnKEc/QWX4hfowepznqNI+CddV9iFuJEmd3RRxs6mgzdjoEsa7Zv5y0W5O0qVxU0A05fyfJFJIv56EbVOpmfpbnNdp2JHI75HG83ucFf12Z06/HezQbh6zOY+Pj+nz/FO8yopUNbcpyg+6jCAoi2VZrWJUNlT1ZnGLYZg1Ndk5VNzZpAm7IYSPKkN716Fapc1tmdShMdpmlRYNIamyUnW5qRYpiTshiuk6ruIVW46HV01prCoptBk/3gJ+WiEROLBouF2Vm2a9adTHDAaHz9iETq2CIs2Iw8oI5q2MmGM5BBu3M0JRFk/j+bxKP2Sx1blWcZH4+kko49sOGHcIASUXe7GrojOaKpcqVstNsWDfsBpoWZ5AAswEkYC7zQDB9wm40sKxTjoxSSiKIoGTFYt8A1DQLkPFiysSPdCOjJiGZ4meKSG7bkZ/Q22YmbYPSAXgIblkhn9sC6s144+QjDJjyxABjTAey7npDf77mqJj9fQ5prSppsAEC71ewg2GzdSxhjWXMAyHOE+QKS0BlL1gmEvObPAropiGJm0r/h2AsZi7SteahjIwEGKL68+WgkTNZkhEvegVvyeCrmwdLcq8rAI7tE5KTtJJvF6nRRIsR9sfL969OY++fvv61bcX0ddvfjrfsSTbt+c/nl/s1Nai7EYsTgrGfRAgumAY7p4gqKdDkf27rbPBTlNobBwMk6qwPf4M6A9aULpv7/C0BHpKYIsZByYyzPlaDMMtRFR7ntSkDzKg4bHj6wYzPMBmNczHJi4WpFeogpyqkYQqExA3VPO7BlcQ/IirKoaypdmssS6pUyCB0uaXtKCvVVzcpOOHxUyeFk46P8yhi00tpDUVBHW4gbAIARvepA1mcFZkFEXYHEUj+P7fX/8josZWFGh3YIoMbGR7AuQNlXXAfSPW1irO5abJqAE5wYwLX1lYyhAX1Sa1miIV5v2ibHQGmnA64dWg3w7MN1mUG0jyo6tiNMa5feoI9qjx6u2LdztYJraAQJ/ehOjOXwGVfmoQ6rKDBaYHNAiSkQC8dt5kvWidQK0CUVJPspqWPJuvPJWFznoZ1hblXxFCBp7zYDjuu5cxPJ+6dd549arYcqsITeEoXrjsOKLsgRQMXWkSRBmU95Hr4TBg/nGo3qd3szxezZOYuKf0d4Ix2QlHbfwIJnaiIeuoTql0CNwAFtwKDBuTCRgcYMDWQHgXjKdKfaZA+OyXEiqRXM3jyg4H8kJFGufRxyxpbkGTsp6gxW17nf2SBmPwZr5ZFXVbTHBrWjXBaai0hcG06gRm5r9/HaknbfQTRYYemnsPhmjASiAyTonJP8usgCwHxTVWWfQlK0ypCnbhlpoc+n1ZpJ6H+4wmTESjeGsptpnVGrJAQURUB/WFABdB2lVTv+KgqsTsCi/bu7FrFgMCB6MsyUQZgGpCO2qJ3U5eXdXNsBm0iqumxlI9gNQJmQNnJHaAwUWzl2t01eynKV2dedMMupqs2KS2UW/z+sbWQyMiQ1kmWw5h3FnDuaqI5o2T0GZ1YLHZg+uaBy0FABry2GO5BkWUEClEnEX93K73YZTdtXXw+0GYuyzNk86GO/BMislghqJ5rTTijMf1OrCgmFH5wpr4vUaYmZXK7/frW69Le3KmP/1Oa8SZ/dYCLhczXCJsI+8Rhjys5weoTRUvTQlo4WBrqjsXdXq2eSWBjY700yJdN8pa9ryqcJ9Sq7QDkDp5BqqEKZdJRjqSyTuR6JEuknGHVblc+Ry8qzS1xME/0BIkLp8T0dfxAPBxAHXP+Ngm/IHVdSpmZbrMPiEnH/kc67q9y1xWkAIhUZpN6iBQXN8VC4U2HAQ7iLGXm/faj+Odb7IctLgv821c99WXB1ll2eQojuWq4CoPLDm2TLXzq5FXb8/Pv99tcdSdLbSoyXnd7mNc2LZKovsHqRZNmgzwGM6tLiYyf/ixHZYhZLDEHGm0A1WDU9qzoup6WM9yt2UfEpfTbUtADeJV0rCc40j9wzskLJ5p8Q4sNwnRZgO6HtfqzojKv7SgMqC4CYBYJzVRokXm3Cvg+q6d6/fVAPZkgtJixDt/s3eiwXXCpKJxaA1if4OvWgC0RhAnfhv7Qar8HXT07vzNmx9+3m1teWoCU3dM1dYMsYMxtlZiE6DSJHom9xvE11xXYzSs23O1PUHyOtEoG44MP7Xj8bGsaEzjgS1UB9/NPyW3QJ/pbtxS2YlpQLrbqT2wU9hy+HsraLDYV4XYXw1HZh+w9kNP9Liz/M5U3BuBgnv/LLLMMsbas8cSjT1BuyJmlGumCo9mwWGdeBEHHXpKIGjXRsdeah1t9ZmTtq5dTLkWHcorNp1/9+LV+fcXL3ZI5TlIQuDGfxjCy/5IOohDx5cHgd6ev9wRZRuna6EAjAm797yMm3GPqQwwIm79Y7RhTDxZ6mIZv2KvdK7x64w/Ts76Dq5MisvqPcjYew/k/jDAgzsd0jsbCTIehdzwdapv9kRM+vGIe8y699g3c0smblixCTe33Cy3c6Hxe4EmncBmclXLzSiQ9E5MYmU4tw06MI+7DKSAODYRYu+2emjM/i7hh+6ohLV3e7AVFNYRI2BhhG3HoHPATU/P3LCrLEmgACeAzn6+Hg9GqFmntu4AR0LRgY6QorWK7Xb3ya3toXatWqwbh/lU3/0+Ik4wCmwA5NPfyJOteFMnqNfvy4eXj3Lh9cM9eHnd6z97DxDxzbbvsFWZbHLcexHFJIq4IYqM3TSBXjjwYNOw0EYQOGjrFUleOpajvcpTcHZjrtP3RZ8ZnrcofvwO8fBwu8kgs63TvUuKti3sEZWr08Xeiahp97SqSn/zhCGNzvsUqnlcp3wBAwqnxWYFkI02+0Szjv3iCZcEZO4p1/Bf5wRK87iRgI+vuu/JzIc0XlhYML9Yad/puC2YjRvtE7yr4MnQb2c+EdDorUoJDxbdqYhFXmZV3dAcCRUYvkprnKBIPAH4JqOdNxW6xlVIIrxi+YFN/DjhWxWbD9IicL1j9VydnZ4eRLmcAtW1h2WiU45EAdjZMPQdc+tc2TkdvdeZqgvY9WaeZwseBXMufqH4pC8Qk+JMX+5FzLGmOcDkCp1OzThta4J7I0tU/eJl4wxwXwBPAlYN9p/97J7qUjdz/OUrMozjaToMpPUZxPH03SMPi60fkNxLsz1a7YVpKzas1D6Ytl49KHjrK7wFzL6WbnpxLtJHSq7BVrH6wvvvxC4iZOpta0wSbhkMB5/2pb7B8wx72ST31lIVnB9DuvTq0yPWHsahYwV3mS6jF+3q+/3hhjXz/r6WFeP/FqaV6pBth/Q5bNzDnAet610E8YssEewPNu7L9uOs/bYVCeU3MK1MT0KThxv2MOOwXfk0/ue4sY8E9SpGFRPvgvEFWKpfDW6K90X5sdD1TE0P8MyTvDWWUmVVmxdhtKpC0Zw1URTUab4M1ZMn7z/G1U0tb9mhYxLRuzNMZ9wv+OklDfP75Ydgxqdn0W2am9NV/GfqnpHAwkcyQ1CG/qtis8jTuEKjKGcMVvi5QBOjEmLntnaJhrio7pRfDX+Mm4DRxjrawi6F+lyPaF57gAgdognU1dkySyGA2uTuTSXEVovTo5y0Xi59ZyANUszHn96hBb9DEGPRQ0P5CNM9vsTQFo8vfRw8vRMwD35/6aPxROjg9T3B9BnxBqPD9qBXmD4ev6dp2+f+DzF9NFi5Pbf2v8X8Bhu6kTbuiQifKi+hNqgdoXXd5AgC2Lu10Jnr4HMFMQkGnizgP34x6tp0FR4vmogu7DlllPgI1e1r/ENR8xqbiDC9yGwiUOmG1WUhTDH6cNdkJDcCPYq/HMH0hz0TDnftH+QjsaepHHOyWSe4n9Rpzt8TamFp+H5h8R9dCGqh+g7xQbDA5tE9Z/5muAj390nEbo548gdjaZym2qRJ9sHaR5h8au/qSFbhHSIaq8/U5wIpTpJHopwIlLy+zZbNo4AA6auv5Orxf0E9fy6gyuqxMP+Suj1eL4GiHx9YKHq/hcFLYevFK71ghCphO6KkjecA9Wg3HMGXmg5PBPFOwI9Lfg85UyPM3KN9KERwAIQz814YTXIACJP0XhgiOADCWXsvjCY5AAS5Zi8K9vdAdC7t4qxOW09J2uUKAh9hvTCjvDDG77X+we/I+e0nH+u0UnHPmY6GrdJJvZkH1ejq09n86vIqOQm+hD/jv6wwfuA/Z21C7U0vjFbq48pgxN3AqEufcAxFz26s15Vlxc9s5X37YlPhERV1aTLvDQEjYpmFFJNlNI8X792H7sbjTWjA1Q+XACgDiNyro/0rD2bs3nqwG/Wbn1AwaRXwgWAu5EvSXIyl7Voe0SKrZqOr02fPLk9XoyNZfdGhNXac2Y6Xr7+zrV/Y1rfnL23r6ZfPzlo4Xv+Z7KeSQrJ+0Wb1Kc4kBRcMkvtZm7tFcuaR4KtKwfyHNrNHcCYJ9GWn5P6j7fzm3QtPpT/Znp+/fX3hDflnYYgX75xhqed/e1abyg=='
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
```

Now you can use `wat`.

## Usage & modifiers
Nuclear comes with the `wat` object that can quickly inspect things
by using the division operator (to avoid typing parentheses). 
A short, no-parentheses syntax `wat / object` is equivalent to `wat(object)`.

You can call `wat.modifiers / object` (or `wat.modifiers(object)`)
with the following **modifiers**:

- `.short` to hide attributes (variables and methods)
- `.long` to show non-abbreviated values and documentation
- `.dunder` to display dunder attributes
- `.code` to reveal the source code of a function, method, or class
- `.nodocs` to hide documentation for functions and classes
- `.all` to include all available information

You can chain modifiers, e.g. `wat.long.dunder / object`.

Call `wat()` to inspect `locals()` variables.

Type `wat` in the interpreter to learn more about this object itself.

## Use cases

### Determine type
In a dynamic typing language like Python, it's often hard to determine the type of an object. WAT Inspector can help you with that by showing the name of the type with the module it comes from.

```python
>>> wat.short({None})
value: {None}
type: set
len: 1
```

### Look up methods
Listing methods, functions and looking up their signature is extremely beneficial to see how to use them.
Plus, you can read their docstrings.

```python
wat('stringy')
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-string.png?raw=true)

### Discover function's signature
See the docstrings and the signature of a function or a method to see how to use it.

```python
wat(str.split)
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-str-split.png?raw=true)

### Look up variables
Check what's inside, list the value of variables and their types to see what's really inside the inspected object.
```python
wat / re.match('(\d)_(.*)', '1_title')
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-re-match.png?raw=true)

### Explore modules
One of the use cases is to explore modules.
For instance you can list functions, classes and the sub-modules of a selected module.

```python
import pathlib
wat / pathlib
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-pathlib.png?raw=true)

Then, you can navigate further, e.g. `wat / pathlib.fnmatch`.

### Explore dunder attributes
```python
wat.dunder / {}
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-dict-dunder.png?raw=true)

### Review the code
Look up the source code of a function to see how it really works.

```python
import re
wat.code / re.match
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/wat-code-rematch.png?raw=true)

### Debug with breakpoint
You can use Python's `breakpoint()` keyword to launch an interactive debugger in your program:

```python
logger.debug('init')
x = {'what is it?'}
breakpoint()
logger.debug('done')
```

```python
(Pdb) from nuclear import wat  # or paste insta-load snippet
(Pdb) wat / x  # inspect local variable
...
(Pdb) c  # continue execution
```

### Explore Python built-ins
```python
wat / __builtins__
```

### Look up local variables
```python
wat()
```


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


# 🐌 Shell utilities

*Nuclear* provides utilities for running system shell commands.

Basic usage:

```python
from nuclear import shell

window_id: str = shell('xdotool getactivewindow')
```

`shell` function captures the stdout & stderr output of the shell command and returns it as a string.
It may also print live stdout in real time (line by line) and capture output in case of errors.

It has a lot of possibilities thanks to its parameters:

* `cmd: str` - shell command to run
* `workdir: Optional[Path] = None` - working directory for the command
* `print_stdout: bool = False` - whether to print live stdout in real time (line by line) from a subprocess
* `print_log: bool = False` - whether to print a log message about running the command
* `raw_output: bool = False` - whether to let subprocess manage stdout/stderr on its own instead of capturing it
* `independent: bool = False` - whether to start an independent process that can outlive the caller process
* `output_file: Optional[Path] = None` - optional file to write the output in real time

It returns the stdout of the command combined with stderr.
In case of non-zero command exit code, `shell` raises `CommandError` exception.
