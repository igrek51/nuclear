## CLI Rules cheatsheet
Here is the cheatsheet for the most important CLI rules:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, arguments, flag, parameter, subcommand, dictionary


def main():
    CliBuilder('hello-app', version='1.0.0', help='welcome', run=say_hello).has(
        flag('--verbose', '-v', help='verbosity', multiple=True),
        parameter('repeat', 'r', help='how many times', type=int, required=False, default=1, choices=[1, 2, 3, 5, 8]),
        argument('name', help='description', required=False, default='world', type=str, choices=['monty', 'python']),
        arguments('cmd', joined_with=' '),
        subcommand('run', help='runs something').has(
            subcommand('now', 'n', run=lambda cmd: print(f'run now: {cmd}')),
        ),
        dictionary('config', 'c', help='configuration', key_type=str, value_type=int)
    ).run()


def say_hello(name: str, verbose: int, repeat: int, cmd: str, config: dict):
    print(f'Hello {name}')


if __name__ == '__main__':
    main()
```

## Complex CLI tree
Here's an example of more complex CLI definition tree:

**multiapp.py**:
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, parameter, flag, subcommand, arguments, default_action
from cliglue.types.filesystem import existing_directory
from cliglue.types.time import iso_datetime


def main():
    CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
               with_defaults=True, help_onerror=False, reraise_error=True, hide_internal=True).has(
        subcommand('git').has(
            subcommand('push', run=git_push).has(
                argument('remote'),
                argument('branch', required=False),
                flag('-u', '--upstream', help='set upstream'),
            ),
            subcommand('help', help='show help', run=lambda: print('show help')),
            subcommand('checkout', 'co', help='checkout branch').has(
                argument('branch', choices=['master', 'feature', 'develop'], type=str),
                flag('force', 'f'),
            ),
            subcommand('remote', help='show remotes list').has(
                subcommand('set-url', 'rename', help="change remote's name").has(
                    argument('remote-name', choices=['origin', 'backup'], type=str),
                    argument('new-name'),
                ),
            ),
            parameter('--date', type=iso_datetime),
            parameter('--count', type=int, required=True),
            parameter('--work-tree', type=existing_directory, default='.', help='working directory'),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=list_screens),
            flag('primary', 'p'),
            default_action(xrandr_run)
        ),
        subcommand('docker').has(
            subcommand('exec', run=docker_exec).has(
                parameter('-u', name='user', type=int),
                argument('container-name'),
                arguments(name='cmd', joined_with=' '),
            ),
        ),
        default_action(lambda: print('default action')),
    ).run()


def git_push(remote: str, branch: str, upstream: bool):
    print(f'git push: {remote}, {branch}, {upstream}')


def xrandr_run(output, primary):
    print(f'xrandr: {output} {primary}')


def list_screens():
    return ['eDP1', 'HDMI2']


def docker_exec(user: int, container_name: str, cmd: str):
    print(f'docker exec {user}, {container_name}, {cmd}')


if __name__ == '__main__':
    main()
```

Usage:
```console
foo@bar:~$ ./multiapp.py --help
multiapp v1.0.0 - many apps launcher

Usage:
  ./multiapp.py [COMMAND] [OPTIONS]

Options:
  --version                        - Print version information and exit
  -h, --help [SUCOMMANDS...]       - Display this help and exit
  --bash-install APP-NAME          - Install script as a bash binary and add autocompletion links
  --bash-autocomplete [CMDLINE...] - Return matching autocompletion proposals

Commands:
  git                                           
  git push REMOTE [BRANCH]                      
  git help                                       - show help
  git co|checkout BRANCH                         - checkout branch
  git remote                                     - show remotes list
  git remote rename|set-url REMOTE-NAME NEW-NAME - change remote's name
  xrandr                                        
  docker                                        
  docker exec CONTAINER-NAME [CMD...]           

Run "./multiapp.py COMMAND --help" for more information on a command.
```

