from nuclear.nuke.config import apply_overrides


class Config:
    dry: bool = False
    bluey_sources: list[str] = [
        'S03/S03E13 Bluey - Podaj Paczkę.mkv',
        'S01/S01E48 Bluey - Dokuczanie.mkv',
        'S02/S02E42 Bluey - Kibel.mkv',
    ]
    bluey_offset: int = 200


def test_load_config():
    dic = {
        'bluey_sources': ['abc'],
        'bluey_offset': 100,
    }
    config: Config = apply_overrides(Config(), Config, dic)
    assert not config.dry
    assert config.bluey_sources == ['abc']
    assert config.bluey_offset == 100


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
    apply_overrides(config, Config, {
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
