import os
from pathlib import Path
from typing import Dict, Type, TypeVar

import yaml

from nuclear import logger

T = TypeVar('T')


def load_config() -> Dict:
    """
    Load general configuration from YAML file given in CONFIG_FILE environment var or load default config.
    :return: loaded configuration dictionary object
    """
    config_file_path = os.environ.get('CONFIG_FILE')
    if not config_file_path:
        logger.warning('CONFIG_FILE unspecified, loading default config')
        return {}

    path = Path(config_file_path)
    if not path.is_file():
        raise FileNotFoundError(f"config file {config_file_path} doesn't exist")

    try:
        with path.open() as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)

            logger.info(f'config loaded from {config_file_path}: {config_dict}')
            return config_dict
    except Exception as e:
        raise RuntimeError('loading config failed') from e


def load_local_config(dataclazz: Type[T]) -> T:
    """
    Load local configuration from YAML file and return it as a dataclass.
    """
    path = Path('.config.yaml')
    if not path.is_file():
        logger.warning(f'Local config not found at {path}, using defaults')
        return dataclazz()

    try:
        with path.open() as file:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)
            config = dataclazz(**config_dict)
            logger.debug(f'local config loaded from {path}: {config_dict}')
            return config
    except Exception as e:
        raise RuntimeError('loading local config failed') from e
