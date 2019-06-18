from typing import Dict, Any, Mapping

from cliglue.parser.keyword import name_from_keyword


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
            return self.__vars[name_from_keyword(key)]


def is_args_container_name(arg: str, annotations: Mapping[str, Any]):
    if arg == 'args':
        if arg in annotations:  # has type annotation
            return annotations[arg] == ArgsContainer
        return True
    return False
