# Inspect

**Nuclear** comes with a powerful inspection tool
that allows you to examine the information about the unknown object.

Open Python Interpreter and run `inspect(object)` on any `object` to inspect 
its type, formatted value, variables, methods, documentation or even source code.

Import inspection tools:
```python
from nuclear import inspect, insp, ins, wat
```

Now, you can call `inspect(object, **options)` with the following `options`:

- `short=True` to hide attributes (variables and methods)
- `dunder=True` to print dunder attributes
- `docs=False` to hide documentation for functions and classes
- `long=True` to print non-abbreviated values and documentation
- `code=True` to print source code of a function, method or class
- `all=True` to include all information

Run `inspect(inspect)` to see more about this function itself.

## Wat inspector
There's a special `wat` object to quickly inspect things, avoiding typing parentheses.

```python
>>> from nuclear import wat
>>> obj = {None}
>>> wat / obj  # Equivalent to: inspect(obj)
>>> wat(all=True) / obj  # Equivalent to: inspect(obj, all=True)
```

## Aliases
Couple of short aliases for `inspect` variants:

```python
from nuclear import inspect, insp, ins

insp(obj)  # Equivalent to: inspect(obj)
ins(obj)  # Short output. Equivalent to: inspect(obj, short=True)
```

## Import
Import inspection tools from **nuclear** package.
```python
from nuclear import inspect, insp, ins, wat
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

and call `inspect` with any object.

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
