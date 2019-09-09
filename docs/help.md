## Auto-generated help
`cliglue` auto-generates help and usage output based on the defined CLI rules.

Let's say we have quite complex CLI definition:
```python
CliBuilder('multiapp', version='1.0.0', help='many apps launcher',
           with_defaults=True, usage_onerror=False, reraise_error=True).has(
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
)
```

We can see the usage and description of commands using `--help` or `-h`:
```console
foo@bar:~$ python3 multiapp.py --help
multiapp v1.0.0 - many apps launcher

Usage:
  multiapp.py [COMMAND] [OPTIONS]

Options:
  --version                        - Print version information and exit
  -h, --help [SUBCOMMANDS...]      - Display this help and exit
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

Run "multiapp.py COMMAND --help" for more information on a command.
```

### Sub-commands help
We can also check the usage for a selected sub-command only:
```console
foo@bar:~$ python3 multiapp.py git --help
multiapp v1.0.0 - many apps launcher

Usage:
  multiapp.py git [COMMAND] [OPTIONS]

Options:
  --date DATE                     
  --count COUNT                   
  --work-tree WORK_TREE            - working directory
  --version                        - Print version information and exit
  -h, --help [SUBCOMMANDS...]      - Display this help and exit

Commands:
  push REMOTE [BRANCH]                      
  help                                       - show help
  co|checkout BRANCH                         - checkout branch
  remote                                     - show remotes list
  remote rename|set-url REMOTE-NAME NEW-NAME - change remote's name

Run "multiapp.py git COMMAND --help" for more information on a command.
```

### version check
Use `--version` in order to show your application version:
```console
foo@bar:~$ python3 multiapp.py --version
multiapp v1.0.0 (cliglue v1.0.1)
```

