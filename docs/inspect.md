# Inspect

*Nuclear* comes with a powerful inspection tool
that allows you to examine the information about the unknown object.

Run `inspect(object)` on any `object` to inspect 
its type, formatted value, variables, methods, documentation or even source code.

```python
from nuclear import inspect

def inspect(
    obj,  # object to inspect
    attrs: bool = True,  # whether to print attributes (variables and methods)
    dunder: bool = False,  # whether to print dunder attributes
    docs: bool = True,  # whether to print documentation
    long: bool = False,  # whether to print non-abbreviated values
    long_docs: bool = False,  # whether to print non-abbreviated documentation
    code: bool = False, # whether to print source code of a function, method or class
    all: bool = False, # whether to include all information
)
```

Run `inspect(inspect)` to see more about this function itself.

## Aliases
There's bunch of short aliases for `inspect` variants:

```python
from nuclear import inspect, insp, ins, insl, insa

inspect(obj)
insp(obj)  # Equivalent to: inspect(obj)
ins(obj)  # Short output. Equivalent to: inspect(obj, attrs=False)
insl(obj)  # Long output. Equivalent to: inspect(obj, long=True, long_docs=True)
insa(obj)  # Show all. Equivalent to: inspect(obj, all=True)
```

## Insta-Load
If you want to debug quickly, you don't even need to install *nuclear* package to use `inspect` function.

Load it on the fly by pasting this snippet:
```python
import base64, zlib
code = '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'
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
```

and do `inspect`
```python
inspect('dupa')
```
