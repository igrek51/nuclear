import sys
from unittest.mock import patch

from nuclear.nuke.config import load_config


def test_e2e_dotted_param_equals():
    """--sub.host=example.com --sub.port=443 overrides nested fields via full load_config pipeline."""
    class SubSettings:
        host: str = 'localhost'
        port: int = 8080
        verbose: bool = False

    class Config:
        dry: bool = False
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--sub.host=example.com', '--sub.port=443', 'deploy']):
        config = load_config(Config)

    assert config.sub.host == 'example.com'
    assert config.sub.port == 443
    assert not config.sub.verbose
    assert not config.dry


def test_e2e_dotted_param_space_separated():
    """--sub.host example.com --sub.port 443 with space-separated values."""
    class SubSettings:
        host: str = 'localhost'
        port: int = 8080

    class Config:
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--sub.host', 'example.com', '--sub.port', '443', 'deploy']):
        config = load_config(Config)

    assert config.sub.host == 'example.com'
    assert config.sub.port == 443


def test_e2e_dotted_bool_flag():
    """--sub.verbose (standalone, no value) flips a nested bool field with default False."""
    class SubSettings:
        verbose: bool = False

    class Config:
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--sub.verbose', 'deploy']):
        config = load_config(Config)

    assert config.sub.verbose


def test_e2e_dotted_bool_explicit():
    """--sub.verbose=true with explicit value."""
    class SubSettings:
        verbose: bool = False

    class Config:
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--sub.verbose=true', 'deploy']):
        config = load_config(Config)

    assert config.sub.verbose


def test_e2e_flat_and_dotted_mixed():
    """Mix flat --dry and dotted --sub.host=example.com in one CLI call."""
    class SubSettings:
        host: str = 'localhost'
        port: int = 8080

    class Config:
        dry: bool = False
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--dry', '--sub.host=example.com', 'deploy']):
        config = load_config(Config)

    assert config.dry
    assert config.sub.host == 'example.com'
    assert config.sub.port == 8080


def test_e2e_dotted_kebab_case():
    """--sub-settings.host-name=value with kebab-case in both segment names."""
    class SubSettings:
        host_name: str = 'default'

    class Config:
        sub_settings: SubSettings = SubSettings()

        def __init__(self):
            self.sub_settings = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', '--sub-settings.host-name=example.com']):
        config = load_config(Config)

    assert config.sub_settings.host_name == 'example.com'


def test_e2e_nested_dict_from_yaml():
    """YAML-style nested dict {sub: {host: yaml.example.com}} via load_config (no CLI overrides)."""
    class SubSettings:
        host: str = 'localhost'
        port: int = 8080

    class Config:
        sub: SubSettings = SubSettings()

        def __init__(self):
            self.sub = SubSettings()

    with patch.object(sys, 'argv', ['nukefile.py', 'deploy']):
        with patch('nuclear.nuke.config._load_local_overrides', return_value={
            'sub': {'host': 'yaml.example.com', 'port': 9090},
        }):
            config = load_config(Config)

    assert config.sub.host == 'yaml.example.com'
    assert config.sub.port == 9090


def test_e2e_dotted_deeply_nested():
    """--outer.inner.value=custom overrides 3 levels deep."""
    class Inner:
        value: str = 'default'

    class Outer:
        inner: Inner = Inner()

    class Config:
        outer: Outer = Outer()

        def __init__(self):
            self.outer = Outer()

    with patch.object(sys, 'argv', ['nukefile.py', '--outer.inner.value=custom']):
        config = load_config(Config)

    assert config.outer.inner.value == 'custom'
