#!/usr/bin/env python3
import re
from typing import List

from cliglue import CliBuilder, parameter, default_action
from cliglue.utils.shell import shell_output


def list_screens() -> List[str]:
    xrandr = shell_output('xrandr 2>/dev/null')
    regex_matcher = re.compile(r'^([a-zA-Z0-9\-]+) connected(.*)')
    return [regex_matcher.sub('\\1', line)
            for line in xrandr.splitlines()
            if regex_matcher.match(line)]


def main():
    CliBuilder('xrandr-demo').has(
        parameter('output', choices=list_screens),
        parameter('mode', choices=['640x480', '800x480', '800x600']),
        default_action(lambda: print('\n'.join(list_screens()))),
    ).run()


if __name__ == '__main__':
    main()
