from typing import Any, Callable, Iterable, TypeVar, List, Union

T = TypeVar('T')


def chunks(lst: List[T], n: int) -> Iterable[List[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def deduplicate_latest(items: list[T], key: Callable[[T], Any]) -> list[T]:
    """Deduplicate items in the list by key. Keep the earliest items first, remove the latest duplicates"""
    ids = set()
    dedup_items: List[T] = []
    for item in items:
        ikey = key(item)
        if ikey not in ids:
            ids.add(ikey)
            dedup_items.append(item)
    return dedup_items


def deduplicate_earliest(items: list[T], key: Callable[[T], Any]) -> list[T]:
    """Deduplicate items in the list by key. Keep the latest items, remove the earliest duplicates"""
    ids = set()
    dedup_items: List[T] = []
    for item in reversed(items):
        ikey = key(item)
        if ikey not in ids:
            ids.add(ikey)
            dedup_items.append(item)
    return dedup_items[::-1]


def flatten(collection: Iterable[Union[T, List[T]]]) -> List[T]:
    """Transform a list of lists into a flat list"""
    flat: List[T] = []
    for item in collection:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat
