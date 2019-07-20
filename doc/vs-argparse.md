## `cliglue` vs `argparse`
Why to use `cliglue`, since we already have Python `argparse`? Here are some subjective advantages of `cliglue`:
- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building - when reading the code, it's easier to distinguish particular CLI rules between them (i.e. flags from positional arguments, parameters or sub-commands),
- CLI definition code as a clear documentation.

### Migrating from `argparse` to `cliglue`

#### Basic CLI
argparse:
```python
import argparse

parser = argparse.ArgumentParser(description='Program description')
[here come the rules...]
args = parser.parse_args()
do_something(args)
```
cliglue:
```python
from cliglue import CliBuilder

CliBuilder(help='Program description', run=do_something).has(
    [here come the rules...]
).run()
```

#### Flags
argparse:
```python
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
```
cliglue:
```python
flag("-v", "--verbose", help="increase output verbosity"),
```

#### Positional arguments
argparse:
```python
parser.add_argument("square", help="display a square of a given number", type=int)
```
cliglue:
```python
argument("square", help="display a square of a given number", type=int),
```

#### Sub-commands
argparse:
```python
def foo(args):
    print(args.x * args.y)

def bar(args):
    print(args.z)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_foo = subparsers.add_parser('foo', help='foo help')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

parser_bar = subparsers.add_parser('bar', help='bar help')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=bar)

args = parser.parse_args()
args.func(args)
```
cliglue:
```python
def foo(args):
    print(args.x * args.y)

def bar(args):
    print(args.z)


CliBuilder().has(
    subcommand('foo', help='foo help', run=foo).has(
        parameter('-x', type=int, default=1),
        argument('y', type=float),
    ),
    subcommand('bar', help='bar help', run=bar).has(
        argument('z'),
    ),
).run()
```

#### Transferring values to functions
argparse:
```python
do_action(args.square, args.verbose)
```
cliglue:
```python
# invoking done automatically
CliBuilder(run=do_action)
```

