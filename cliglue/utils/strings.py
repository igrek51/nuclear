from typing import List, Union

from .output import fatal


def nonempty_lines(str_in):
    all_lines = str_in.splitlines()
    return list(filter(lambda l: len(l) > 0, all_lines))


def split_to_tuple(line, attrs_count=None, splitter='\t'):
    parts = line.split(splitter)
    if attrs_count and len(parts) != attrs_count:
        fatal('invalid split parts count (found: {}, expected: {}) in line: {}'.format(len(parts), attrs_count, line))
    return tuple(parts)


def split_to_tuples(lines: Union[List[str], str], attrs_count=None, splitter='\t'):
    if not isinstance(lines, list):
        lines = nonempty_lines(lines)
    return list(map(lambda line: split_to_tuple(line, attrs_count, splitter), lines))
