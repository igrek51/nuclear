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
code = 'eJzNGltuG0fyX6doKB8cSjQjxfsAGNO7Sqw4Bhx7YStrGJIwGZJNaeLhDDE9tCxzCeQQe4Y92J5kq6pf1fMgKW8+IkAkp7veVV1d1dPzsliIWVIl0yxRSiqRLpZFWfmhAzOQ5mopp5VIlFDVLDaPdrZwcKW0v9S9Opgj+ep+meY3lvJZfj8Qz9JpNRAvUwWfr5dVWuRJNhAX90s5EC8qWSaTDH79nMPEwd+9LPQpXmje3xf5PL0ZHQj4U7dAeiQmRZHR82yVz2TJB4qpYo9Zkd+wx2kxk+axi9tZVZXpZFVJzTBPFoChqpKePibZCh5BNXoEheEJtdHUkyxDhbbJtyzTj0nFQVR6kyfVqoQxa6FL4Hdt1akPz+TcOikimGLyK4k0oKejQd1QYix+SDIlBw2JajPOdDB+Ua7MsDdhCO5tGY6DEerDfW3Lw8ND+j7/lCzSXIrqVqLwoEgP4jGfF+UiQU0HQq2mtxiBaaXIyAOhJys50z4YwFeZorHVQCxkdVvMlNNitZB5RZREUQpVrMqpJHGHBDFaJmWy0GbT7EVVWJNyCGPDu1ugL0sEAu/llR4XxaparipxlwJz+E5s3CgR5TIlDCejyEEQI2afs7DeaPDQE4xqgEWeauIEqoPFxHyVT/FBiSSfCbP0OSXt3AalvMgfJZNJKT+mibO5JhIw4aR0PDSN5c0virlInEzWb+gjvQ4ZMQoiRivNp9kKKMA4j5QgrIhfZPwYaxi9QswqGWjPjelzYEw8NpYGKYD4gCwyxg83gtYe44cbQWXGWiMaISb9vl2akVuR4ujow11S3ii/Akya8YFvpJGZJLOW95STRzbOdfi7JGGVtRmAqUVL1nPkiSKwxh8oX/TFo6eYXEcGAhM9zAaJP+p2GvMNcxzzj15reqWOaBuiHAosLnV+haeYDA1Dxkj6GQ2rsUu5NDC0DwAgjvj5dM5AxHiMQDSLwRHOxDCVLuNpkRVl5Fib2PCSDpPlUuazaN5bv714//I8/u7Ni+c/XsTfvfz5fKMlWb85f3t+sRFrR2XT0+JIMOyDCKL5u8ntSQT19FT4/GbtbbAxEIY2MsPwZrbHx4g+0ILcfVvZ00YcKIEjlg+kFFhZirHRIwSkAk8a0AcZ0OI4/mbAsgeyqYKFWCX5VOoFG2VUEc2oOgJxB2JyX+FWhl9JWSaQOqrVEmsjJQEEyqvPMqefZZLfyP7DYiaTuZcuDHOY0qZm0to6hiY8IyyFwIY3ssJdSSvSi2McjuMe/P7vb/9hUeNSFtodkGJLNnYzEeIOhHPAvhHrKibvcjtk1YCcYPnCTy0sZQhMVE5ThKKdkTLNkJI8PbdbQGMMp8UKNpreVd7r46o+8QBbFHj+5uz9BrL3GijQd7AUmiuXkZKfKiR12aDVowQI4dFjBK+9H7VWtFGhVhEr6Iepok3XZapAZaaz2b+NLfVTjCSjwG3ATs/tZYzAm75AsP68ytd6lAVlXlRWIb1XOT6s8oLkC1NyFsUpNBexn9EBoPH7A/FB3o+zZDGZJYQ9os8hRmMjEI3xY1jSM0NSxUpSCRN5Bo64ExjaoiEYHMiArQHwPuqPhPhKgPDp5wJ2+kxMktKxA3mhKE6y+C6dVbegSaGGaHE3rtLPMuqDN7PVIld1McGtsqyik4EwFgbTimNYk//+rSeO6tSPBRm6a9U9mEQFVgKRcUkMfy3SHPIb1PdYgdKPNLfVMthFjyhy6Ksil4GH24zGTERcgl0Ux+w+Des/JyAqfdpCwFRl2lWjsM6gWsT2pJf1bvBaiwGBg1E2S1kBgGrCOGqJ015eU1mOcRi0SspKYbcQQdKEzIErEifA4Gw4yDWmBwBAFv2mIAuWGUxVab6SbtC0mW28DWukqEk5JFcIYdw5w/l6iNaNl9Dlc0Bx2UNXNA/aBIDoQPPu890npoRIIeItGmZ1UyJTXjfWwd87ydynMps1Gv4oMCkmgzGKFowSx7HmG0xgKTGmwkVrEs5aYcZOqnA+rGqDKePJsfkOJ50Rx+5XjXAxxfLYD+q2oMvDZn2A2lTr0pKAER1sVXnvo86stqAYcNEhP03lshLOsudliY2SErJBQHp5OuqDkS6QrHQkU3Ai0iJdzOMO63G+83nyvsY0Ekf/REuQuPqUin72OwgfRlDx9A9dwu/YXUdsVcp5+gkx9ZHToanYm8hFCSkQEqVtljsJJeo+nwq0YSexnTS2Yusm/ctwJ6s0Ay32Rb5NVFtluROVl00e4pDvCr7ywJJjraE2YTXy/M35+avNGrluXKFFQ97rroPxYVsrifYPUiMaNxnQ0+T87mIj8/XbelgOIIPN7ElMPVANcUp7TlRTCZtV7hv1LnF1uq0JaIgENTRs58ipnb2nhMUzbd6RwyYh6mgA1+JaMxlT+SdzKgPymwiATVJjJVpsj94iXd/Vc/22GsCdR1BajHXPb7smYm4SJhWNXXuQ9jf4qkaA9gjCxF/9MEhF2DvH789fvnz9brN25akNTDMxEmvLYgM81k5iG6DcJGYltxsk1NxUY8TWd1t1T5C8XjTKhj2LT+N4fM0rGju4o4Vq0PfrT/AW6CszjS2VW5iWSLOd2kJ2BC1H2FvBgKN9lbP+qjsy2wgbP7REj3+X0FiKWyOQYW9fRQ6Zx1h99TigfiBoU8SUcs1I4JkuOKwRL+yIwywJJNq00WGQWntrc9pkrOs2U12LduUVl85/Ont+/uribINQgYM4CWz5u0kE2R9BO+nQoeVOQm/On20Isk6naaEIjAnde1YkVb/FVJYwUlyHB2jdNPFMqUnL+hVnuXOtX8f66/i07cjKprhUbaGMs3tQbg8DPLIzIb1xkcDjkckNP0fmvSKLyTAescdUrQe+qd8ysWHFIWxu9TBv5wbW7zmadAjN5ELxZhRAWhcmoWpyvg3asY6bCKQAOzZhYm/WhjVmf5/wB/6oRGvve7AFFNaxpoCFEY4dgs6RHnp06tku0tkMCnAi0OjnVb8zQu0+tfYHOJwUHegwKWq72GazT26ts9rUarFmHGYj8+b5C+IEo8AFQDb6nTxZizdxjHr9sXx4+UUuvH64By+vW/3n3gDE+s166LBFMVtl2HsRxDCO9UAcW7sZALNx4MGmRaFGEDCo9Yo5Lh3LUa/yCJxd2df526LPstctShi/XTia3WbYiezq9OD1RN0W7ojK1+msdyJo6p4miZIqbJ8wqHFYv3UxuqIkBjYsl4CqBwbz6TeWIQz+NQ6f8E8fsQROdcTCUqP+LsY3UM7rxqL4jkGHcruVdD9vqNfqHDwW9GcajvI8LVVFET4QYLZSKlxeCDwE8lVKfTOVqdbQCMIs6vABjT0c67chbjXLPPKzffFUnJ6c7KRyOQKo64CWjS3OicKnUe63HVKbTNc429zrRNSH23I1ydKp5oIZE39QbNEPCCt2Is87CXsoaY8fdX1NZ1466RqAvSlzqua+zMobYF8CgQRaNege29ED1blu9vAqVKSbTqBpNyGjTyedQN8t8mixzQ2UvTTbotVWMnXFupXaRqauVwsVfFvLvAXIoZZ+eelcZA6E/ICrQc2L6n8QOouQUdCU2ARaMxgyH7Wlvs7TCPeqiHfGXBVcH126tOrTItYWxK5DAf8SnEcv2jX0+8MNa9f9vpZl/H8P03J1yLZd+uw27m7MndYNXuPoK1Us2B9s3Gf1i2LbbcsSyu9gWp6emCYPN+xuxG676rP0d0lVv2NVIGndw+IdMmmuHa7yD3lxl5t6RtENPujxPkLHizcGl7DfAaq9aEX7KhS9aRXHkZLZvHGpC/9wYhjT3TVMaHqe4dMdGI0fFiAMGa+vxbcys6ej+Gcrnx6jhddbukhZ+Cf5aprJpESzCG8OrfJTRo1xJYqNt61zNMRFeS9+CcvZOyD8tSFoIu6XQQtQdHRU0Mmy6jfgMbm0YGggtLPFdAj+oibEmwhRA9pDc54NcalPLoPzBn2lbMcBEDK7TWc8b4nIX+nEeGdXOgP65n3eHgy6b3uGBPGe2/ZzJifu/tdAAxZ0gr23xA+4IRpwoat5e3N50OXRgA+UCvuw6bpXCkEfvKkw+W7nFQW2cDquKeCfvqnqx0ztnkyrmF7S6zRT4OVX3w2FB6Hu/icC4VLhGYhRpbeqPnNhWqpdTfUc6Br+ZQ9SBnRayO46PLxH4LBDNEIQWX711AJ0nsG/o8TAwbW0FbgHUrETmNlg5F6YkabMXATUhx7+a0YpU7fpvPoiQkDpyROevP8vUk+fMlJF+aVk/sV1+3K9DjBvj8n+ffytzIO/Qmz751r0tjTPhl0ph2o1icre1afTydXl1ew4+hY++n9bYMMO/zrQadGJce/q5PHjy5NF74CvTjqowolTN/HsxU9u9Bs3ClnPjZ58+/i0RieYP+XztPw56jd11BDilEPoHYZjP65j10BOAxC8ScWQ/1RHDgBOOYB5wcGx/+wmv39/Fqj0Fzfz7scXFwHLvzJDnL33hqWZ/wFUTp4e'
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
