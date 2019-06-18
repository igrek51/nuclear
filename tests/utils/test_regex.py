from cliglue.utils.files import save_file
from cliglue.utils.regex import *


def test_regex_replace():
    assert regex_replace('abca', 'a', 'b') == 'bbcb'
    assert regex_replace('abc123a', r'\d', '5') == 'abc555a'


def test_regex_match():
    assert regex_match('ab 12 def 123', r'.*\d{2}')
    assert not regex_match('ab 1 def 1m2', r'.*\d{2}.*')


def test_regex_list():
    # regexReplaceList
    assert regex_replace_list(['a', 'b', '25', 'c'], r'\d+', '7') == ['a', 'b', '7', 'c']
    assert regex_replace_list(['a1', '2b', '3', ''], r'\d', '7') == ['a7', '7b', '7', '']
    assert regex_replace_list(['a1', '2b', '3', ''], r'.*\d.*', '7') == ['7', '7', '7', '']
    # regexFilterLines
    assert regex_filter_list(['a1', '2b', '3', ''], r'.*\d.*') == ['a1', '2b', '3']
    assert regex_filter_list(['a1', '2b', '3', ''], r'dupa') == []
    # regexSearchFile
    assert regex_search_file('tests/utils/res/findme', r'\t*<author>(\w*)</author>', 1) == 'Anonim'
    assert regex_search_file('tests/utils/res/findme', r'\t*<name>(\w*)</name><sur>(\w*)</sur>', 2) == 'Sur'
    # regexReplaceFile
    save_file('tests/utils/res/replaceme', 'dupa\n123')
    assert regex_replace_file('tests/utils/res/replaceme', r'[a-z]+', 'letters') == 'letters\n123'
