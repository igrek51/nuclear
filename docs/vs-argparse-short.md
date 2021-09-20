## `nuclear` vs `argparse`
Why use `nuclear`, since Python already has `argparse`? Here are some subjective advantages of `nuclear`:

- declarative way of CLI logic in one place,
- autocompletion out of the box,
- easier way of building multilevel sub-commands,
- automatic action binding & injecting arguments, no need to pass `args` to functions manually,
- CLI logic separated from the application logic, 
- simpler & concise CLI building - when reading the code, it's easier to distinguish particular CLI rules between them (i.e. flags from positional arguments, parameters or sub-commands),
- CLI definition code as a clear documentation.

Sub-commands done with `argparse`:
```python
def foo(args):
    print(args.x * args.y)

def bar_go(args):
    print(args.z)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

def _print_help(_: argparse.Namespace):
    parser.print_help(sys.stderr)

parser.set_defaults(func=_print_help)

parser_foo = subparsers.add_parser('foo', help='foo help')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo)

parser_bar = subparsers.add_parser('bar', help='"bar" help')
subparsers_bar = parser_bar.add_subparsers()

parser_bar_go = subparsers_bar.add_parser('go', help='"bar go" help')
parser_bar_go.add_argument('z')
parser_bar_go.set_defaults(func=bar_go)

args = parser.parse_args()
args.func(args)
```
with nuclear it's much simpler and cleaner:
```python
def foo(x, y):
    print(x * y)

def bar_go(z):
    print(z)


CliBuilder().has(
    subcommand('foo', help='foo help', run=foo).has(
        parameter('-x', type=int, default=1),
        argument('y', type=float),
    ),
    subcommand('bar', help='"bar" help').has(
        subcommand('go', help='"bar go" help', run=bar_go).has(
            argument('z'),
        ),
    ),
).run()
```

