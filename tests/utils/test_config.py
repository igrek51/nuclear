import os
from contextlib import contextmanager
from dataclasses import dataclass

from nuclear.utils.config import load_local_config


@dataclass
class LocalConfig:
    url: str = 'https://igrek51.github.io'
    git_ref: str = 'master'


def test_load_local_config():
    with change_dir('tests/utils/res'):
        local_config = load_local_config(LocalConfig)
        assert local_config.url == 'https://github.com/igrek51/nuclear'
        assert local_config.git_ref == 'master'


@contextmanager
def change_dir(dir: str):
    previous_dir = os.getcwd()
    try:
        os.chdir(dir)
    except FileNotFoundError as e:
        print(f'Current dir is: {previous_dir}')
        raise e
    try:
        yield
    finally:
        os.chdir(previous_dir)
