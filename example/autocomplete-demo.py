#!/usr/bin/env python3
import re
from typing import List

from nuclear import CliBuilder, flag, parameter, subcommand, argument, shell, shell_output


def main():
    CliBuilder('autocomplete-demo').has(
        subcommand('adjust', run=adjust_screen, help='change screen resolution').has(
            argument('output', choices=list_screens, required=True, help='screen output name'),
            parameter('mode', choices=['640x480', '800x480', '800x600'], required=True, help='resolution mode'),
            flag('primary', help='set output as primary'),
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
