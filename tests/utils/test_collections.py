from nuclear.utils.collections import chunks, deduplicate_latest, deduplicate_earliest, flatten


def test_chunks():
    assert list(chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert list(chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)) == [[1, 2, 3, 4], [5, 6, 7, 8], [9]]


def test_deduplicate_latest():
    assert deduplicate_latest([1, 2, 3, 1, 4, 5, 6, 7, 8, 8], lambda x: x) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert deduplicate_latest([1, 2, 3, 1, 4, 5, 6, 7, 8, 9], lambda x: x % 3) == [1, 2, 3]


def test_deduplicate_earliest():
    assert deduplicate_earliest([1, 2, 3, 1, 4, 5, 6, 7, 8, 8], lambda x: x) == [2, 3, 1, 4, 5, 6, 7, 8]
    assert deduplicate_earliest([1, 2, 3, 1, 4, 5, 6, 7, 8, 9], lambda x: x % 3) == [7, 8, 9]


def test_flatten():
    assert flatten([1, [2, 3], [4, [5, 6], 7], 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten([[1, 2], [3, 4], [5, 6], [7, 8]]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten([1, 2, 3, 4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten([]) == []
    assert flatten([1, [2, 3], 4, [5, 6], 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten([1, [2, 3], 4, [5, 6], 7, 8, [9, 10, 11]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert flatten([1, [2, 3], 4, [5, 6], 7, 8, [9, 10, 11], 12]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert flatten([1, [2, 3], 4, [5, 6], 7, 8, [9, 10, 11], 12, 13]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
