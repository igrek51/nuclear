from typing import Set


def trim_dashes(arg: str) -> str:
    while arg.startswith('-'):
        arg = arg[1:]
    return arg


def name_from_keyword(keyword: str) -> str:
    return trim_dashes(keyword).lower().replace('-', '_')


def keyword_from_name(name: str) -> str:
    if name.startswith('-'):
        return name
    if len(name) == 1:
        return '-' + name
    else:
        return '--' + name


def names_from_keywords(keywords: Set[str]) -> Set[str]:
    return set([name_from_keyword(k) for k in keywords])


def keywords_from_names(names: Set[str]) -> Set[str]:
    return set([keyword_from_name(name) for name in names])
