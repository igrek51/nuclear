### Sub-commands
Commands may build a multilevel tree with nested sub-commands (similar to `git`, `nmcli` or `ip` syntax).

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


TODO
```python
"""
    Create Subcommand rule specification.
    Subcommand is a keyword which narrows down the context and can execute an action.
    Subcommands may have multiple levels and may build a tree.
    It's similar to 'git' syntax: 'git remote rename ...'
    Subcommand can have more subrules which are activated only when corresponding subcommand is active.
    Subrules can be added using 'has' method.
    :param keywords: keyword arguments which any of them triggers a subcommand
    :param run: optional action to be invoked when subcommand is matched
    :param help: description of the subcommand displayed in help output
    :return: new subcommand rule specification
    """
```
    