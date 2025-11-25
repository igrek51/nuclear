from nuclear.nuke.invoke import parse_cli_args, apply_cli_overrides


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


def test_apply_cli_overrides():
    class Config:
        dry: bool = False
        bluey_sources: list[str] = [
            'S03/S03E13 Bluey - Podaj Paczkę.mkv',
            'S01/S01E48 Bluey - Dokuczanie.mkv',
            'S02/S02E42 Bluey - Kibel.mkv',
        ]
        bluey_offset: int = 200
        flag: bool = False
        truth: bool = True
    
    config = Config()
    apply_cli_overrides(config, {
        'dry': '1',
        'bluey_sources': '["42"]',
        'bluey_offset': '10',
        'flag': 'True',
        'truth': 'false',
    })
    assert config.dry
    assert config.bluey_sources == ['42']
    assert config.bluey_offset == 10
    assert config.flag
    assert not config.truth
