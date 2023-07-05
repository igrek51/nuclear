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
code = 'eJzNGu1u20byv59i4f4QZTOq3dwHoEa5cxs3DZAmB8e9ILANlpJWNhuKFEgqjqIT0Ie4Z7gHuye5mdmvWX5Isq8/GiAyuTvfMzszu9xZkc/FNK7iSRqXpSxFMl/kReWGDvRAkpULOalEXIqymkb61czmFq6Q5qlclQczJF+tFkl2ayifZatQvEgmVSheJyX8vl1USZ7FaSguVwsZileVLOJxCk8/ZzBx8HcnC/2KV4r393k2S26HBwL+lXdAeijGeZ7S+3SZTWXBB/JJyV7TPLtlr5N8KvVrF7ezqiqS8bKSimEWzwGjrAp6+xSnS3gF1egVFIY31EZRj9MUFdom36JIPsUVBymT2yyulgWMGQtdAb8bo059eCpnxkkBweTjX0mkkN6OwrqhxEj8EKelDBsS1Was6WD8sljqYWdCH9zZ0h8HI9SH+8qWh4eH9Pf8czxPMimqO4nCgyI9iMdslhfzGDUNRbmc3GEEJlVJRg6FmqzkVPkghD9FgsYuQzGX1V0+La0Wy7nMKqIk8kKU+bKYSBJ3QBDDRVzEc2U2xV5UuTEph9A2vL8D+rJAIPBeVqlxkS+rxbIS9wkwh7+xiZtSBJlMCMPKKDIQRIvZ5yyMNxo81ASj6mGRp5o4nupgMTFbZhN8KUWcTYVe+pyScm6DUpZnT+LxuJCfktjaXBHxmHBSKh6axnLmF/lMxFYm4zf0kVqHjBgFEaOVZJN0CRRgnEeKF1bEL9B+jBSMWiF6lYTKcyP6DbWJR9rSIAUQD8kiI/yxI2jtEf7YEVRmpDSiEWLS79ulGdglKY6OPt7HxW3ploDOMy7yeeS4iEFbm4gxGpplT7pYyobtw7hqI8hUkjeLFZWCoVleatXZ3NQqgbImZYqmNA0n/IHSVF88eY45faghsL7ArFdvgu5YYSHB4oWFhVriwCAiawJpbQn1jtZzIGhpBoGvAf0glAJTqWZIdZSKAMBf2cie9dbvLj+8Po++u3j18sfL6LvXP59vVKVaX5y/O7/ciLWVZdMLtyNSTbN43vyH89ev377frI3UGw2mSaqKlYD3S/B/FWcTqeIkSKn+T6kXAORQjFcVJm78ExdFDBFbLRfYCZQSQKCZ+CIzeizi7Fb2dRg7UwzixUJm06BVg1RmTgHf8DClzLrp9Y20pmrThGOEhR/MfCsrXJ9KkV4U4XAU9eD5v7/9RxPxqji6EpAiQzayMwHihsI6f091XH/gvGmGjBoQioYvPCphKTBxfVhNEYrqAAX4gFIavbdbQGEMJvkS0mrvOuv1xWgkThzAFgVeXpx92EDSWAMF+qsjxWkuYSW2kpKfKyR11aDVo3UH4dFjBG+cH5VWlJZRq4C1r4OkpBJDGlLB4SoznXW10rZUbxGSDDy3ATs1t5cxPG+6cmj8eZ2t1SgLyiyvjEIqRVo+rFqMQIgCynMQJdBKR25GBYDC74fio1yN0ng+nsaEPaTfAUZjIxC18aNCYqIjkmVUSirYgWNgiVuBYRMwAIMDGbA1AK6C/lCIrwQIn3zJocCkYhwXlh3ICy1gnEb3ybS6A03ycoAWt+Nl8kUGffBmupxnZV1McKssquAkFNrCYFpxDGvy37/1xFGd+rEgQ3etugeTqMBKIDIuicGveZJBfoNuFvstekgy0xuCXdRISQ59k2fS83Cb0ZiJiEsECTNZQAymeRHgmKJQSFj/GQFRxW0LAd0MKFcN/fJGJdDswK7qe58bJQYEDkbZNClc+KOaMI5a4rSTV/dRIxwGreKiKrE3DiBpQubAFYkTYHA27OUa3fECIIt+3Qd4ywymqiRbSjuoN1VtvDVrpKhIWSRbmjHurOFchaZ14yS0+RxQbPYg4IcVASAaKt59Xn0iSogUIs6iflbXnRnldW0dfN5JZpXIdNrY3gaeSTEZjFA0b5Q4jhRfbwKr/4iaFKWJP2uEGVmp/Hm/mfKmtCdH+q8/aY04sk81wvkEuzI3qLrRLg/r9QFq0w6flgSMqGCripWLOr3avGbARof8PJGLSljLnhcFbgtKIRsEpJOnoz8YqgbJSEcyefv/FukiHncA41U+R971k1ri4J9oCRJXncnQY7+D8GEAHU//0Cb8juo6ZKtSzpLPiKkOWBSqTJvIeQEpEBKl2Rp2EorLVTYRaMNOYjtpbMVWO67H4Y6XSQpa7It8F5dtneVOVN42OYhDXhVc54Etx1pBbfxu5OXF+fmbzRq5bmyjRUPO67bBd2Fba4n2D1ItGjcZ0FPkXHUxkfn2XT0sQ8hgU3PuUA9UTZzSnhVVd8J6lbv9YZe4Kt3WBNREvB4ayjlyamfvKGHzTMU7sNgkRB0N4Fpcqycjav9kRm1AdhsAsE5qrEWLzLFBoPq7eq7f1gPYbTClRWTDNqPEXCdMahq7apDyN/iqRoBqBGHiU98PUtGxv7TtqQlMPTEUa8NiAzzWVmIToNwkeiW3G8TXXHdjxNbttuqeIHmdaJQNewafxvGwlnc0ZnDHFqpB360/wbdAX+lp3FLZhWmINLdTW8gOYcvh761gwNK+ztj+qjsy2whrP7REjzs5byzFrRHIsLevIovMY6y+eixQ3xO0KWJCuWYo8AQTHNaIF3bEoZcEEm3a6NBLrb21PoPR1rXFVPWiXXnFpvOfzl6ev7k82yCU5yBOArf83SS87I+gnXTorGwnoYvzFxuCrNNpWigAY8LuPc3jqt9iKkMYKWo77aaJZ0pNWsavOMuda/w6Un+OT/vdlPHMqpsyzu5B2Ra9woQwDzsmHjwO9ccyFnp+2OFWsqwdAuozN1cZcV+KQ7iHVcN81xYa92ZouQHsGecl33MCSOv6I1RFzu12dizXJgIpwE5HmNibtWaNSd7l9dCdiCjt3VZrDv1zpChg/4Njh6BzoIaenDq282Q6hT6bCDS27WW/MxBNOVq7cxpOis5tmBS1YrXZ7JNC66w2tZarGW7pUH9OfUScYBTYAEiHv5Mna/EmjlGvP5YPrx7lwpuHe/DqptV/9lA/Up+LfYfN8+kyxS0WQQyiSA1EkbGbBtD1Ac8vDQrt9wCDdlgRx6XTN9qSPAFnV+Yb9bboM+zVTsSP3y4cxW4z6EQmM9TKMJ5auS23tcMsKcqKPBOKKASWJYYFAg8WcVEltK2jLsoYBkGcTxw+oLGXY3VYb6NQZoGb7Yvn4vTkZCeVqyFA3Xi0jE04J1K70Y22naHqFdo4etvrwM7tWhbLcZpMFBdc6fhAC50ewPXswJg3uubMzJyOqfaPjmRUstAAe1PmVPXlhaUzwL4EPAmUarC5aUf3VOe6mbMVX5FuOp6m3YS0Pp10PH23yKPE1h9399Jsi1ZbydQV61ZqG5m6Xi1UYJR7C5B9Ld3yUqeR+rzCDdhOWfWVm38QOouQodczm2pWMxgy93dBinr3Ztl+yeAbN64Kro8uXVr1aRFrC2LXntWmOC960a6+3x9uWLPu97Us4/97mJarQ7bt0me3cXdj7rSu95VB3W9hwf5g476o39rZbluWUH4H0/L0xDR5uGF3I3bbVR31vo8re/PkQsZQ+j5JU85y5KH2WnizR+rLYMvsY5bfZ/qCSmkunFAlhfYsqaIoKGU6a1xuwX84MYjo6hCmMDXP8Au5KDS+33IwZLw9FN3J1BzX4T9d4Xs9RgtvP3SRMvDPsuUklXGBhmB6K92eM2qMK1FsfP6boSEui5X4xW+87oHw15qgjrFfwhag4Ogop6POst+Ax3TSgqGA0M4G0yK4e3IQYcJH9WgP9AErRKI6SvPOQdTVmh0nEsjsLpnyTNV1P6pOX39g2oNB92U7nyDe99l+8GHF3f8WnseCjlT3lvgBF/Q8LnRFaW8uD7q75/GB5mAfNl3X+iDovaNzneF2fjNnC6fjuzn+UxcF3Zju1iFNRfTVWKWZHO8euu8b/smcvQeHQLhUeAZiVOkzn8tcmJZqV/QcB7oFfdWDlNELid2Nf5qMwJ6mRggiy6/gGYDOQ+H3lBg4uJK2AvdMk09WYGaDoT3MIk2ZuQioD7vNrxmltLxLZtWjCAGlZ8948v6/SD1/zkjlxWPJ/Ivr9ni9DjBvj8j++iywHqYt+2JNt5CDcjkOit7159Px9dX19Dj4Fn76f5vjdTT4ryKaVpcY9a5Pnj69Opn3DvgypLMTnDi1Ey9e/WRHv7GjkN7s6Mm3T09rdLz5Uz5P65yjflNH9SFOOYQqJRz7aR27BnLqgeAdHob8pzqyB3DKAfTROsf+s538/sOZp9Jf7Mz7H19deiz/ygxx9sEZlmb+BzxawfI='
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
