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
