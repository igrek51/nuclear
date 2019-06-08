import re
from typing import List, Union

from .files import read_file
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


def regex_match(str_in, regex_match_pattern):
    return bool(re.compile(regex_match_pattern).match(str_in))


def regex_replace(str_in, regex_match_pattern, regex_replace_pattern):
    return re.compile(regex_match_pattern).sub(regex_replace_pattern, str_in)


def regex_filter_list(lines, regex_match_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return list(filter(lambda line: regex_matcher.match(line), lines))


def regex_replace_list(lines, regex_match_pattern, regex_replace_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return list(map(lambda line: regex_matcher.sub(regex_replace_pattern, line), lines))


def regex_search_file(file_path, regex_match_pattern, group_number):
    regex_matcher = re.compile(regex_match_pattern)
    with open(file_path) as f:
        for line in f:
            match = regex_matcher.match(line)
            if match:
                return match.group(group_number)


def regex_replace_file(file_path, regex_match_pattern, regex_replace_pattern):
    file_content = read_file(file_path)
    lines = nonempty_lines(file_content)
    lines = regex_replace_list(lines, regex_match_pattern, regex_replace_pattern)
    return '\n'.join(lines)
