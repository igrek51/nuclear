from typing import Dict, Any

from nuclear.parser.keyword import format_var_name


class ArgsContainer(object):
    def __init__(self, _vars: Dict[str, Any]):
        self.__vars = _vars

    def __getattr__(self, name):
        if name in self.__vars:
            return self.__vars[name]
        else:
            raise AttributeError

    def __getitem__(self, key):
        if key in self.__vars:
            return self.__vars[key]
        else:
            return self.__vars[format_var_name(key)]
