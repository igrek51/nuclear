# Inspect

*Nuclear* comes with a powerful inspection tool
that allows you to examine the information about the unknown object.

Open Python Interpreter and run `inspect(object)` on any `object` to inspect 
its type, formatted value, variables, methods, documentation or even source code.

```python
from nuclear import inspect

def inspect(
    obj,  # object to inspect
    attrs: bool = True,  # whether to print attributes (variables and methods)
    dunder: bool = False,  # whether to print dunder attributes
    docs: bool = True,  # whether to print documentation
    long: bool = False,  # whether to print non-abbreviated values
    full_docs: bool = False,  # whether to print non-abbreviated documentation
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
insl(obj)  # Long output. Equivalent to: inspect(obj, long=True, full_docs=True)
insa(obj)  # Show all. Equivalent to: inspect(obj, all=True)
```

## Insta-Load
If you want to debug quickly, you don't even need to install *nuclear* package to use `inspect` function.

Load it on the fly by pasting this snippet to your Python interpreter:
```python
import base64, zlib
code = 'eJzVGttu20b2PV8xcB9EJoxgNXsBVKi7bqNNDbhJ4Xi3MGyDoMSRzZYiBZJKrAoC8hH9hn5Yv2TPOXMfkpIc5GG3QGVy5tzvM8yiKpcsTZpknid1zWuWLVdl1ZilZ3IhK+oVnzcsqVndpLF8Vbulhqu4eqo39bMFkm82q6y4V5TPik3EXmfzJmIXWQ2/71ZNVhZJHrGrzYpH7LzhVTLL+bN/GiHol50Lpt+XxSK7Hz9j8F/SNFU9ZrOyzOk9XRcpr+yFcm7v52Vx773GHsi8TLl87ZPgDLhms3XDhRBFsgSMuqno7UOSr+EV9KRX0B7eUDVBPclz1G6fzKsq+5A0Nkid3RdJs65gTZnrBvjdKRX95ZQvlMcCgilnv5BIEb09j3zjsQm7qtY8agkEG/9K8lrtaFM5CMaqLrhnXnfT2NldBwP5y6Gw88nJCf2dPibLrOCseeCoGCg5gMAtFmW1TNAKEavX8wcM1aypyQERE5sNT4V/IvhTZeiIOmJL3jyUaa1VXC950RAlVlasLtfVnJO4Q4IYr5IqWQqTCvasKZW5bQhp348PQJ9XCASeLRpap/CpWaDFYEmRKklCm4ryRouM2LCoOVhk9TaOrZ0NL1zYgi/K4mUym1X8Q5Zo49U+YtzDzcfu5S5ioYVvmZ6VC5awxbqYCw8LS6F/RH7aZscAsmhlxTxfAwVYt6PECSniF0gfxgJGZI7Mnkh4c0K/yBaoRdIFE+kJtYommeCPgQP7TPBHrWjS2nwT/aSxUO+JUJ5WwlAndqATmj1//uvHpLqvTZKo/NC5cTjglB1U0SCNNWXF9mlcec7J2dWG2kknC2FUkeZtfvnnqil8wAIvAEMZv6Q6mrpTJnIfFTfLO+K9JWFylIQYeV2Fqtsked7HrRWc/ydlPWQvv8X+OJYQ2L9h1+nngZVfXmJZ+WMlV9SVO1bSiCIKXGNyOvCTphPvaGwDgk3CgsDXgH4QSoCV62a1bsY0tVCXBfgbnceLwfb91fXFNP7u8vzND1fxdxf/nu7EKLC9nL6fXu3YVsuyG0T7EWlo0Hhi/3p6cfHu591WibuT+5KWmAWyhZ4wSPSx5qNHCFTznjexgov1DmIM4xjHmTiOmDaQ0X6YrFa8SINOoc2QYjRWS7tBqCJN8YdHL99CpQJCYYqKSBlSqB2S5M3l2fUOEuq22AL87haTS1lIE5YEqaYig8CaZYdZTa2E7EaNxTakbUnRlaQa4i1GkoFjMWAn9gzmsYY0bU+ZErQSq21lRLprHlatn4AAFZS9IM5gpo7NjrC7wA8j9ivfTPJkOUsTwh7T7xDDoOV//tig2HHFMTGJZB3XnJpyYNdfSVwLC6eBIRgbyICdAXAThGPGvmIPZZX9VkKXyNksqTQ7kBcqZ5LHH7O0eQBNynqI1tbrdfYbD0LwZL5eFrUvJriUV01wGjFpXTAre8EGf/7+acCe+9RfMDJyX7A/mUQDVgKRB7fFYPhLmRVBjk0ASgujh6yQDNAuYqWGUalhb8vC5AAudBnNMhFxiaEeZCuIv7ysAlwTFCoOaVcQEHWPrhCQfUu4auyWYyrZ6ih245977oQYEDgYZWlWmdBHNWEdtcRtI6+qwuBGFEPEIIAYs+uKBFA6+QjNwMhRa4KYYJukauqPWfMQDOJ4EFJO4wa4zVrWyPJg1YUtkdHqgsWTCieQi4SCoV2CY5iBak5+NQq4FVCeRqgGyoTWzewgrU3G87R1KA2ceoNpPEH5nFViOxHMnQ3sLBPqfEIdd1cJM9FSuftu23a2pO0n8q+7qS050U8e4XKO/d8sipmozx/6RB7pEYkC2jkli9Bsqo2J0dh2NsA4/cHpk7Ky8cc5XzUs+A8aa1pVZSWuMegx7CF8Evz56Y/wRJfGnh40tuKWL7JHxKRdgcnzNm5ZQa2AiqLOSb10knpTzBmYUNGqeReYBpDlxLQr7FNbAagnFNnD3lxOp293W/TBTjdnWjJW0MOLcaPXSI93mpTNNgXQE+RMXVKeevfed1MEGZSqU6nvOEmc0k6LKkcXWT/NmNwnrsh5T0BJxBl6oBEgp272hhL8DqnsBxqbhPDRAK7DvXIzrh9wOiiogRT3AQDLpLKae6yOi4GYDPxas6976IGfKgmysSZsYi4ncRo3egphqC/RPAJUowgTn0I3SpkXkmp21oPNzh2qx2yrWOyAx1ZLrALUNok4M/cYxNVc9nFia8Zj3xMkrxGNqsNA4dM6XvH1Y5msGjN7Gv5K7uM8rPOtNx666EntO3xmbjlbCbDX7xb2/tjVyLZn/ZjVQKEjaFvEjDJ8zPBWacJOW17KasjMJinmXHVkJNq20YlT0AZbeZyT1tUlXcw6fdmsq+iPZ2+mb6/OdgjlOMgmgSejfhJCEITpJUCH8H4Kl9PXOwLxCbRtEoD5IrbIy6QJO4xjU5SWOUwzzeZNm5byJO7a7lSenIg/L0ZhP+UcDur9lHH3CMq6uVQqaO1As8SDx7H8rmEFmxtoOOzX3g2CPLebDoQnB1zCU4ZYtufqSPm1QMsNYapf1vapAEA6M45QBTkzDx9I0DYCKWCdXS2xd1vJGouQqZ+ROa8K7c1cvYS5LRYUcNbAtRPQORBLL0eG7TJLU5jviEDrYFWHvYGoyv7WnKJtUnSqtqTwmsLuqKLps9p5o0073PKx/PL1GXGCUaADIB9/IU968Qan2cXgf8yHN5/lwrune/DmrtN/+kYwFh/zXIcty3Sd42hPEMM4FgtxrOwmAWRHwNslhULnDMCgyT62cel+ZLbO8uYlOLtRXxD3RZ9iL67w3PjtwxHsdsNeZDKD13jxXoEOWK4dFllVN+SZiMURsKwxLBB4uILDdkZnEnS9DigEMT4x+IBmveC9y6c/dBfJeRGY3ZB9y0anpwep3IwB6s6hpWxicyK1W1Nf1y2XzNDW5chRVyrmdLBaz/JsLrhgpuMDJTo9gOutKz17oFS3GereQsx6dPQWxUICHE3Zpio/La+NAY4l4EggVINDRDe6o7qtmzrTu4r003E07Sck9eml4+i7Rx4htvx4dpRme7TaS8ZXrF+pfWR8vTqowKrtLUB2tTTpJW6d5Kcrs6BnY3Hm2v1E6FaEjJ0pWXUzz2DI3L0wF9T7D6X6rtm+ebdVwfzo06VTnw6x9iD2nQ11iXOiF+3q+v3phlV5f6xlLf5fwrS2OmTbPn0OG/cw5kHrqm9E8h9D4IddK9ifbNzX/j+q2G9bq6B8AdPa5cnS5OmGPYzYb1fR7r2PCh29XvbOig/r9SyoBrePo9ntzW36IvgGfsJ/LAcRG8D/4psEGZFNBrenr17dnC4Hz2yr0zyIGyO98fr8R736tV6Fk6VePf3m1cij4+yP7H06JtuoX/uoLsTIhhCTko39ysf2QEYOCH45spD/4iM7ACMbQF4Q2Nh/1ZvfX585Kv1N7/z8w/mVw/LvliHOro1haee/x5rGdQ=='
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
```

and call `inspect` with any object.

## Use cases
### Look up methods
List methods or functions and look up their signature to see how to use them.
Plus, see their docstrings documentation.

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

### Discover function usage
See the docstrings and the signature of a function or a method to see how to use it.

```python
inspect(str.split)
```

### See function code
Look up the source code of a function to see how it works.

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
