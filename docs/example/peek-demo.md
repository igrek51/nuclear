ipython3
```python
from cliglue import CliBuilder, flag, parameter

cli = CliBuilder(run=lambda force: print(f'force is {force}'))

cli.has(
    flag('force'),
)

cli.run_with_args(['--force'])
```

./autocomplete-demo.py

subl ./autocomplete-demo.py
```python
#!/usr/bin/env python3
import re
from typing import List

from cliglue import CliBuilder, flag, parameter, subcommand, argument
from cliglue.utils.shell import shell, shell_output


def main():
    CliBuilder('autocomplete-demo').has(
        subcommand('adjust', run=adjust_screen).has(
            argument('output', choices=list_screens, required=True, help='screen output name'),
            parameter('mode', choices=['640x480', '800x480', '800x600'], required=True),
            flag('primary'),
        )
    ).run()


def list_screens() -> List[str]:
    """Return list of available screen names from a system"""
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def adjust_screen(output: str, mode: str):
    shell(f'echo xrandr --output {output} --mode {mode}')


if __name__ == '__main__':
    main()
```

sudo ./autocomplete-demo.py --install-bash autocomplete-demo

bash

autcom[Tab]

autocomplete-demo [Tab][Tab]

autocomplete-demo --h[Tab]

autocomplete-demo a[Tab] --h[Tab]

autocomplete-demo adjust [Tab][Tab]

autocomplete-demo adjust H[Tab]

autocomplete-demo adjust HDMI-1 --m[Tab] --mode[Tab][Tab] --mode [Tab][Tab]

autocomplete-demo adjust HDMI-1 --mode 8[Tab] 800x6[Tab]

autocomplete-demo adjust HDMI-1 --mode=800x600