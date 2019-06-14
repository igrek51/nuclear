import re

from .strings import nonempty_lines
from .files import read_file


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
