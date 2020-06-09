## Quick start
Let's create a simple command-line application using `cliglue`.
Let's assume we already have our fancy functions as follows:
```python
def say_hello(name: str, decode: bool, repeat: int):
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))

def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x ** 2, n, x)) if (x in r) else r),
                        range(2, int(n ** 0.5)), set(range(2, n)))))
```
and we need a "glue" which binds them with a CLI (Command-Line Interface).
We want it to be run with different keywords and parameters provided by user to the terminal shell in a following manner:
- `./quickstart.py hello NAME --decode --repeat=3` mapped to `say_hello` function,
- `./quickstart.py calculate factorial N` mapped to `calculate_factorial` function,
- `./quickstart.py calculate primes N` mapped to `calculate_primes` function,

We've just identified 2 main commands in a program: `hello` and `calculate` (which in turn contains 2 subcommands: `factorial` & `primes`). That forms a tree:
- `hello` command has one positional argument `NAME`, one boolean flag `decode` and one numerical parameter `repeat`.
- `calculate` command has 2 another subcommands:
    * `factorial` subcommand has one positional argument `N`,
    * `primes` subcommand has one positional argument `N`,

So our CLI definition may be declared using `cliglue` in a following way:
```python
CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        flag('decode', help='Decode name as base64'),
        parameter('repeat', type=int, default=1),
    ),
    subcommand('calculate').has(
        subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
            argument('n', type=int),
        ),
        subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
            argument('n', type=int, required=False, default=100, help='maximum number to check'),
        ),
    ),
)
```
Getting it all together, we've bound our function with a Command-Line Interface:

**quickstart.py**:
```python
#!/usr/bin/env python3
import base64
from functools import reduce
from cliglue import CliBuilder, argument, flag, parameter, subcommand

def say_hello(name: str, decode: bool, repeat: int):
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))

def calculate_factorial(n: int):
    print(reduce(lambda x, y: x * y, range(1, n + 1)))

def calculate_primes(n: int):
    print(sorted(reduce((lambda r, x: r - set(range(x ** 2, n, x)) if (x in r) else r),
                        range(2, int(n ** 0.5)), set(range(2, n)))))

CliBuilder().has(
    subcommand('hello', run=say_hello).has(
        argument('name'),
        flag('decode', help='Decode name as base64'),
        parameter('repeat', type=int, default=1),
    ),
    subcommand('calculate').has(
        subcommand('factorial', help='Calculate factorial', run=calculate_factorial).has(
            argument('n', type=int),
        ),
        subcommand('primes', help='List prime numbers using Sieve of Eratosthenes', run=calculate_primes).has(
            argument('n', type=int, required=False, default=100, help='maximum number to check'),
        ),
    ),
).run()
```

Let's trace what is happening here:

- `CliBuilder()` builds CLI tree for entire application.
- `.has(...)` allows to embed other nested rules inside that builder. Returns `CliBuilder` itself for further building.
- `subcommand('hello', run=say_hello)` binds `hello` command to `say_hello` function. From now, it will be invoked when `hello` command occurrs.
- `subcommand.has(...)` embeds nested subrules on lower level for that subcommand only.
- `argument('name')` declares positional argument. From now, first CLI argument (after binary name and commands) will be recognized as `name` variable.
- `flag('decode')` binds `--decode` keyword to a flag named `decode`. So as it may be used later on. Providing `help` adds description to help screen.
- `parameter('repeat', type=int, default=1)` binds `--repeat` keyword to a parameter named `repeat`, which type is `int` and its default value is `1`.
- Finally, invoking `.run()` does all the magic.
It gets system arguments list, starts to process them and invokes most relevant action.

### Help / Usage
`CliBuilder` has some basic options added by default, e.g. `--help`.
Thus, you can check the usage by running application with `--help` flag:
```console
foo@bar:~$ ./quickstart.py --help
Usage:
./quickstart.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...] - Display this help and exit
  --bash-install APP_NAME     - Install this program in bash to be executable from anywhere, add autocompletion links

Commands:
  hello NAME           
  calculate factorial N - Calculate factorial
  calculate primes [N]  - List prime numbers using Sieve of Eratosthenes

Run "./quickstart.py COMMAND --help" for more information on a command.
```

As prompted, we can check more detailed subcommand helps:
```console
foo@bar:~$ ./quickstart.py hello --help
Usage:
./quickstart.py hello [OPTIONS] NAME

Arguments:
   NAME

Options:
  --decode                    - Decode name as base64
  --repeat REPEAT             - Default: 1
  -h, --help [SUBCOMMANDS...] - Display this help and exit
  --bash-install APP_NAME     - Install this program in bash to be executable from anywhere, add autocompletion links
```

### Injecting parameters
Let's invoke `say_hello` function on a first run.

Now when we execute our application with required argument provided, we get:
```console
foo@bar:~$ ./quickstart.py hello world
I'm a world!
```
Note that `world` has been recognized as `name` argument.
We've binded `say_hello` as a default action, so it has been invoked with particular parameters:
```python
say_hello(name='world', decode=False, repeat=1)
```

- positional argument `name` has been assigned a `'world'` value.
- flag `decode` was not given, so it's `False` by default.
- parameter `repeat` was not given either, so it was set to its default value `1`.

Let's provide all of the parameters explicitly, then we get:
```console
foo@bar:~$ ./quickstart.py hello UGlja2xl --decode --repeat=3
I'm a Pickle! I'm a Pickle! I'm a Pickle!
```
Or we can do the same in arbitrary order:
```console
foo@bar:~$ ./quickstart.py hello --repeat 3 --decode UGlja2xl
I'm a Pickle! I'm a Pickle! I'm a Pickle!
```

Invoking other subcommands is just as easy:
```console
foo@bar:~$ ./quickstart.py calculate primes 50
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49]
```

When you are writing function for your action and you need to access some of the variables (flags, parameters, arguments, etc.),
just simply add a parameter to the function with a name same as the variable you need.
Then, the proper value will be parsed and injected by `cliglue`.

