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

- `attr=False` to hide attributes (variables and methods)
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
ins(obj)  # Short output. Equivalent to: inspect(obj, attr=False)
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
