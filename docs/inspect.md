# Inspect

**Nuclear** comes with a powerful inspection tool
that allows you to examine the information about the unknown object.

Open Python Interpreter and run `inspect(object)` on any `object` to inspect 
its type, formatted value, variables, methods, documentation or even source code.

You can call `inspect(object, **options)` with the following `options`:

- `short=True` to hide attributes (variables and methods)
- `dunder=True` to print dunder attributes
- `docs=False` to hide documentation for functions and classes
- `long=True` to print non-abbreviated values and documentation
- `code=True` to print source code of a function, method or class
- `all=True` to include all information

Run `inspect(inspect)` to see more about this function itself.

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
