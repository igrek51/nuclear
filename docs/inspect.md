# Nuclear Inspect

**Nuclear** comes with a powerful inspection tool
that allows you to delve into and examine unknown objects at runtime.

Start the Python Interpreter and execute `wat / object` on any `object` to investigate
its type, formatted value, variables, methods, documentation, and even source code.

<video width="100%" src="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect.mp4" controls="true" allowfullscreen="true" poster="https://raw.githubusercontent.com/igrek51/nuclear/master/docs/demo/demo-inspect-poster.png"></video>

You can call `inspect(object, **options)` or `wat(**options) / object` with the following `options`:

- `short=True` to hide attributes (variables and methods)
- `dunder=True` to display dunder attributes
- `docs=False` to hide documentation for functions and classes
- `long=True` to show non-abbreviated values and documentation
- `code=True` to reveal the source code of a function, method, or class
- `all=True` to include all available information

Execute `inspect(inspect)` to learn more about this function itself.

## Import
Import inspection tools from **nuclear** package.
```sh
pip install nuclear
```
```python
from nuclear import inspect, ins, wat, wats
```

Alternatively, use **Insta-Load** in the section below.

### Insta-Load
If you want to debug something quickly, you don't even need to install **nuclear** package to use `inspect` and `wat` functions.

Load it on the fly by pasting this snippet to your Python interpreter:
```python
import base64, zlib
code = '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'
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
```

and call `inspect` or `wat` with any object.

## WAT inspector
There's a special `wat` object to quickly inspect things, avoiding typing parentheses.

```python
>>> from nuclear import wat
>>> obj = {None}
>>> wat / obj  # Equivalent to: inspect(obj)
>>> wat(all=True) / obj  # Equivalent to: inspect(obj, all=True)
```

## Aliases
Couple of short aliases for `inspect` and `wat` variants:

```python
from nuclear import inspect, ins, wat, wats

ins(obj)  # Short output. Equivalent to: inspect(obj, short=True)
wats / obj  #Short output. Equivalent to: wat(short=True) / obj
```

## Use cases

### Look up methods
Listing methods, functions and looking up their signature is extremely beneficial to see how to use them.
Plus, you can see their docstrings documentation.

```python
inspect('dupa')
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/inspect-methods.png?raw=true)

### Determine type
In a dynamic typing language like Python, it's often hard to determine the type of an object.
`inspect` can help you with that by showing the name of the type with the module it comes from.

```python
>>> inspect({None})
value: {None}
type: set
```

### Explore modules
One of the use cases is to explore modules.
For instance you can list functions, classes and the sub-modules of a selected module.

```python
import nuclear
inspect(nuclear)
```

![](https://github.com/igrek51/nuclear/blob/master/docs/img/inspect-modules.png?raw=true)

Then, you can navigate further, eg. `inspect(nuclear.sublog)`.

### Look up variables
List the value of variables and their types to see what's really inside the inspected object.

```python
wat / 42
```

### Discover function usage
See the docstrings and the signature of a function or a method to see how to use it.

```python
inspect(str.split)
```

### Review the code
Look up the source code of a function to see how it really works.

```python
>>> from nuclear import inspect, CliBuilder
>>> inspect(CliBuilder().run, code=True)
─────────────────────────────────────────────────────────────────────────────────────────────────────
value: <bound method CliBuilder.run of <nuclear.builder.builder.CliBuilder object at 0x7f8936d57b80>>
type: method
signature: def run()
"""
Parse all the CLI arguments passed to application.
Then invoke triggered action which were defined before.
If actions need some parameters, they will be injected based on the parsed arguments.
"""
source code:
    def run(self):
        """
        Parse all the CLI arguments passed to application.
        Then invoke triggered action which were defined before.
        If actions need some parameters, they will be injected based on the parsed arguments.
        """
        if self.__log_error:
            with logerr():
                self.run_with_args(sys.argv[1:])
        else:
            self.run_with_args(sys.argv[1:])
```

### Usage with breakpoint
You can use Python's `breakpoint()` keyword to launch an interactive debugger in your program:

```python
logger.debug('init')
x = {'what is it?'}
breakpoint()
logger.debug('done')
```

```python
(Pdb) from nuclear import wat
(Pdb) wat / x  # inspect
...
(Pdb) c  # continue execution
```
