#!/usr/bin/env python3
from nuclear import CliBuilder, parameter
from typing import List


def what_to_skip(skip: List[str]):
    print(f'skipping: {skip}')


CliBuilder(run=what_to_skip).has(
    parameter('skip', multiple=True, type=str),
).run()
