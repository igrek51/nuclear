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
