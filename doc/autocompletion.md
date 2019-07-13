## Auto-completion
Shell autocompletion allows to suggest most relevant hints on hitting `Tab` key.

Auto-completion provided by `cliglue` is enabled by default to all known keywords based on the declared subcommands and options.

Defining possible choices may imporove auto-completing arguments. You can declare explicit possible values list or a function which provides such a list at runtime.

**completers.py**:
```python
#!/usr/bin/env python3
import re
from typing import List

from cliglue import CliBuilder, parameter, default_action
from cliglue.utils.shell import shell, shell_output


def list_screens() -> List[str]:
    """Return list of available screen names in a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def adjust_screen(output: str, mode: str):
    shell(f'xrandr --output {output} --mode {mode}')


CliBuilder('completers-demo').has(
    parameter('output', choices=list_screens, required=True),
    parameter('mode', choices=['640x480', '800x480', '800x600'], required=True),
    default_action(adjust_screen),
).run()
```

In order to enable auto-completion, you need to install some extension to bash. Fortunately `cliglue` has built-in tools to do that:
```console
foo@bar:~$ sudo ./completers.py --bash-install completers-demo
[info]  creating link: /usr/bin/completers-demo -> ~/cliglue/doc/example/completers.py
#!/bin/bash
_autocomplete_98246661() {
COMPREPLY=( $(completers-demo --bash-autocomplete "${COMP_LINE}") )
}
complete -F _autocomplete_98246661 completers-demo
[info]  Autocompleter has been installed in /etc/bash_completion.d/autocomplete_completers-demo.sh. Please restart your shell.
```
Now, we have `completers-demo` application installed in `/usr/bin/` (symbolic link to the current script) and bash completion script installed as well.
We can hit `[Tab]` key to complete command when typing. Here are some completions examples:
```console
foo@bar:~$ completers-d[Tab]
foo@bar:~$ completers-demo

foo@bar:~$ completers-demo [Tab][Tab]
--bash-autocomplete  -h                   --mode               --output
--bash-install       --help               --mode=              --output=

foo@bar:~$ completers-demo --mo[Tab]
foo@bar:~$ completers-demo --mode

foo@bar:~$ completers-demo --mode [Tab][Tab]
640x480  800x480  800x600

foo@bar:~$ completers-demo --mode 640[Tab]
foo@bar:~$ completers-demo --mode 640x480

foo@bar:~$ completers-demo --mode 640x480 --output [Tab][Tab]
eDP-1   HDMI-1
```

### Custom completers
You can provide your custom auto-completers (providers of possible values) to the `choices` parameter.

The example is the function which returns a list of available screens:
```python
def list_screens() -> List[str]:
    """Return list of available screen names in a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]
```
You can use it to validate and propose available choices for parameter or positional argument:
```python
CliBuilder().has(
    parameter('output', choices=list_screens, required=True),
)
```

### Installing Autocompletion
In order to enable the autocompletion, there must be a specific script in `/etc/bash_completion.d/`.
With `cliglue` you just need to run:
```console
# sudo ./sample-app.py --bash-install sample-app
```
It will install autocompletion script and add a symbolic link in `/usr/bin/`,
so as you can run your app with `sample-app` command instead of `./sample_app.py`.

Now you can type `sample-app` and hit `Tab` to see what are the possible commands and options.

If you type `sample-app --he`, it will automatically fill the only possible option: `--help`.

Sometimes, you need to make some modifications in your code,
but after these modifications you will NOT need to reinstall autocompletion again.
You had to do it only once, because autocompletion script only redirects its query and run `sample_app.py`:
```console
sample-app --bash-autocomplete "sample-app --he"
```

### How does auto-completion work?
1. While typing a command in `bash`, you hit `Tab` key. (`your-app.py cmd[TAB]`)
2. `bash` looks for an autocompletion script in `/etc/bash_completion.d/`.
There should be a script installed for your command after running `--bash-install` on your application.
So when it's found, this script is called by bash.
3. The autocompletion script redirects to your application, running it with `--bash-autocomplete` option, namely script runs `your-app.py --bash-autocomplete "cmd"`, asking it for returning the most relevant command proposals.
Notice that in that manner, the autocompletion algorithm is being run always in up-to-date version.
4. `your-app.py` has `--bash-autocomplete` option enabled by default so it starts to analyze which keyword from your CLI definition is the most relevant to the currently typed word (`cmd`).
5. `your-app.py` returns a list of proposals to the `bash`.
6. `bash` shows you these results.
If there's only one matching proposal, the currently typed word is automatically filled.

