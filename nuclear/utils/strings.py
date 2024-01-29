import re
from typing import List, Union, Optional


def nonempty_lines(str_in: str) -> List[str]:
    all_lines = str_in.splitlines()
    return list(filter(lambda l: len(l) > 0, all_lines))


def split_to_tuple(line: str, attrs_count: Optional[int] = None, splitter: str = '\t'):
    parts = line.split(splitter)
    if attrs_count and len(parts) != attrs_count:
        raise RuntimeError(f'invalid split parts count (found: {len(parts)}, expected: {attrs_count}) in line: {line}')
    return tuple(parts)


def split_to_tuples(lines: Union[List[str], str], attrs_count=None, splitter='\t'):
    if not isinstance(lines, list):
        lines = nonempty_lines(lines)
    return list(map(lambda line: split_to_tuple(line, attrs_count, splitter), lines))


def format_bytes(count: int):
    """Format bytes amount as a human friendly string with KiB, MiB, GiB"""
    if count == 1:
        return '1 byte'
    elif count < 1024:
        return f'{count} bytes'
    elif count < 1024**2:
        return f'{count/1024:.2f} KiB'
    elif count < 1024**3:
        return f'{count/1024/1024:.2f} MiB'
    else:
        return f'{count/1024/1024/1024:.2f} GiB'


def strip_ansi_colors(content: str) -> str:
    """Remove ANSI escape codes controlling font colors"""
    return re.sub(r'\x1b\[\d+(;\d+)?m', '', content)
