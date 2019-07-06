## Quick start
Let's create simple command-line application using `cliglue`.
Let's assume we have a function as follows:
```python
def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)
```
and we need a glue which binds it with a CLI.
We want it to be run with different parameters provided by user to the terminal shell in a manner:
`./hello.py WORLD --reverse --repeat=1`.
We've identified one positional argument, a flag and a numerical parameter.
So our CLI definition may be declared using `cliglue`:
```python
CliBuilder('hello-app', run=say_hello).has(
    argument('name'),
    flag('reverse'),
    parameter('repeat', type=int, default=1),
)
```
Getting all together, we've binded our function with a CLI definition:

**hello.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, flag, parameter


def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)


def main():
    CliBuilder('hello-app', run=say_hello).has(
        argument('name'),
        flag('reverse'),
        parameter('repeat', type=int, default=1),
    ).run()


if __name__ == '__main__':
    main()
```

Let's trace what is happening here:
- `CliBuilder` is used to build CLI tree for entire application.
- `'hello-app'` is a name for that application to be displayed in help output.
- `run=say_hello` sets default action for the application. Now a function `say_hello` is binded as a main action and will be invoked if no other action is matched.
- `.has(...)` allows to embed other rules inside that builder.
- `argument('name')` declares positional argument. From now, first CLI argument (after binary name) will be recognized as `name` variable.
- `flag('reverse')` binds `--reverse` keyword to a flag named `reverse`. So as it may be used later on.
- `parameter('repeat', type=int, default=1)` binds `--repeat` keyword to a parameter named `repeat`, which type is `int` and its default value is `1`.

Finally, invoking `.run()` does all the magic.
It gets system arguments list, starts to process them and invokes corresponding action.

### Help / Usage
`CliBuilder` has some basic options added by default, like `--help` or `--version`.
Thus, you can check the usage by running application with `--help` flag:
```console
foo@bar:~$ ./hello.py --help
hello-app

Usage:
  ./hello.py [OPTIONS] NAME

Options:
  -h, --help [SUCOMMANDS...]       - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals
  --reverse                       
  --repeat REPEAT                 
```

Notice there are already rules being displayed, which were declared before:
- positional argument `name`: `./hello.py [OPTIONS] NAME`
- flag `reverse`: `--reverse`
- parameter `repeat`: `--repeat REPEAT`

### Injecting parameters

Now when we execute our application with one argument provided, we get:
```console
foo@bar:~$ ./hello.py world
Hello world.
```
Note that `world` was matched to `name` argument.
We've binded `say_hello` as a default action, so it has been invoked with particular parameters:
```python
say_hello(name='world', reverse=False, repeat=1)
```
- positional argument `name` has been assigned a `'world'` value.
- flag `reverse` was not given, so it's `False` by default.
- parameter `repeat` was not given either, so it was set to its default value `1`.

Let's provide all of the parameters explicitly, then we get:
```console
foo@bar:~$ ./hello.py --reverse world --repeat 2
Hello dlrow.Hello dlrow.
```
Or we can do the same in a different way:
```console
foo@bar:~$ ./hello.py world --repeat=2 --reverse
Hello dlrow.Hello dlrow.
```
