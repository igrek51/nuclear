from typing import Set


def trim_dashes(arg: str) -> str:
    while arg.startswith('-'):
        arg = arg[1:]
    return arg


def format_var_name(keyword: str) -> str:
    return trim_dashes(keyword).lower().replace('-', '_')


def format_keyword(name: str) -> str:
    name = name.lower().replace('_', '-')
    if name.startswith('-'):
        return name
    if len(name) == 1:
        return '-' + name
    else:
        return '--' + name


def format_var_names(keywords: Set[str]) -> Set[str]:
    return set([format_var_name(k) for k in keywords])


def format_keywords(names: Set[str]) -> Set[str]:
    return set([format_keyword(name) for name in names])
