from nuclear.nuke.config import load_config_from_dict


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
    config: Config = load_config_from_dict(Config, dic)
    assert config.dry == False
    assert config.bluey_sources == ['abc']
    assert config.bluey_offset == 100
