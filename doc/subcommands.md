## Sub-commands
Commands may form a multilevel tree with nested sub-commands.

Sub-commands syntax is commonly known:
- `git remote rename ...`,
- `docker container ls`,
- `nmcli device wifi list`,
- `ip address show`.

Sub-commands split the CLI into many nested CLI levels, forming a tree.
They decide where to direct the parser, which seeks for a most relevant action to invoke.

Sub-commands create a nested levels of sub-parsers, which not only may have different actions but also contains different CLI rules, such as named parameters, flags or other sub-commands, which are only enabled when parent command is enabled as well.
Subcommand can have more subrules which are activated only when corresponding subcommand is active.
So subcommand is just a keyword which narrows down the context.

### Sub-commands specification
In order to create subcommand rule specification, use:
```python
from cliglue import subcommand

subcommand(
        *keywords: str,
        run: Optional[Action] = None,
        help: str = None,
)
```

`keywords` - possible keyword arguments which any of them triggers a subcommand

`run` - optional action to be invoked when subcommand is matched

`help` - description of the parameter displayed in help output

### Nesting sub-commands
With sub-commands, you can nest other CLI rules.
They will be active only when corresponding subcommand is active.

Subrules can be nested using `.has(*subrules: CliRule)` method.
It returns itself for further building, so it can be used just like `CliBuilder`:
```python
from cliglue import CliBuilder, argument, subcommand

CliBuilder().has(
    subcommand('nmcli').has(
        subcommand('device').has(
            subcommand('wifi').has(
                subcommand('list'),
            ),
        ),
    ),
    subcommand('ip').has(
        subcommand('address', 'a').has(
            subcommand('show'),
            subcommand('del').has(
                argument('interface'),
            ),
        ),
    ),
)
```
In that manner, the formatted code above is composing a visual tree, which is clear.

### Sub-commands example
**subcommands.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, subcommand


def main():
    CliBuilder('subcommands-demo', run=lambda: print('default action')).has(
        subcommand('remote', run=lambda: print('action remote')).has(
            subcommand('push', run=lambda: print('action remote push')),
            subcommand('rename', run=lambda: print('action remote rename')),
        ),
        subcommand('checkout', run=lambda: print('action checkout')),
        subcommand('branch', run=lambda: print('action branch')),
    ).run()


if __name__ == '__main__':
    main()
```
Usage is quite self-describing:
```console
foo@bar:~$ ./subcommands.py remote
action remote
foo@bar:~$ ./subcommands.py remote push
action remote push
foo@bar:~$ ./subcommands.py branch
action branch
foo@bar:~$ ./subcommands.py
default action
foo@bar:~$ ./subcommands.py --help
subcommands-demo

Usage:
  ./subcommands.py [COMMAND] [OPTIONS]

Options:
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  remote        - List remotes
  remote push  
  remote rename
  checkout      - Switch branches
  branch        - List branches

Run "./subcommands.py COMMAND --help" for more information on a command.
```

See [sub-commands tests](../tests/parser/test_subcommand.py) for specification.

