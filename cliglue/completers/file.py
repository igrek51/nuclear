import os
from typing import Optional, Tuple


def file_completer(current: Optional[str]):
    listdir, prefixdir = _current_listing_dir(current)
    names = []
    for file in os.listdir(listdir):
        filepath = f'{prefixdir}{file}'
        if os.path.isdir(filepath):
            names.append(f'{filepath}')
        else:
            names.append(filepath)
    return sorted(names)


def _current_listing_dir(current: Optional[str]) -> Tuple[str, str]:
    if not current:
        return '.', ''

    current_path, current_node = os.path.split(current)
    if not current_path or current_path == '.':
        return '.', ''

    if not os.path.isdir(current_path):
        return '.', ''

    return current_path, f'{current_path}/'
