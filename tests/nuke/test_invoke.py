from nuclear.nuke.invoke import parse_cli_args


def test_parse_cli_args():
    positional, overrides = parse_cli_args(['--name=value', 'pos1', '--flag', 'pos2', '--long-name="long value"'])
    assert positional == ['pos1', 'pos2']
    assert overrides == {
        'name': 'value',
        'flag': '1',
        'long_name': 'long value',
    }


def test_parse_cli_args_kebab_case():
    positional, overrides = parse_cli_args(['--kebab-case=value', '--another-flag'])
    assert positional == []
    assert overrides == {
        'kebab_case': 'value',
        'another_flag': '1',
    }


def test_parse_cli_args_empty():
    positional, overrides = parse_cli_args([])
    assert positional == []
    assert overrides == {}


def test_parse_cli_args_only_positional():
    positional, overrides = parse_cli_args(['pos1', 'pos2'])
    assert positional == ['pos1', 'pos2']
    assert overrides == {}
