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
code = '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'
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
