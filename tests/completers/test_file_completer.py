from pathlib import Path

from nuclear import *
from nuclear.completers import file_completer
from tests.asserts import MockIO


def test_file_completer_empty():
    with MockIO('--autocomplete', '"app "') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = mockio.stripped().splitlines()
        assert '.gitignore' in proposals
        assert 'tests' in proposals

        assert 'tests/' not in proposals
        assert 'tests/autocomplete' not in proposals
        assert 'tests/__init__.py' not in proposals
        assert '.' not in proposals
        assert '..' not in proposals


def test_file_completer_file():
    with MockIO('--autocomplete', '"app .gitignore"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        assert mockio.stripped() == '.gitignore'


def test_file_completer_dir1():
    with MockIO('--autocomplete', '"app tests"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = set(mockio.stripped().splitlines())
        assert proposals == {'tests'}


def test_file_completer_dir_content():
    with MockIO('--autocomplete', '"app tests/"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = mockio.stripped().splitlines()
        assert 'tests/autocomplete' in proposals
        assert 'tests/__init__.py' in proposals

        assert 'tests/' not in proposals
        assert 'tests/autocomplete/' not in proposals
        assert '.gitignore' not in proposals
        assert '.' not in proposals
        assert '..' not in proposals


def test_file_completer_subdir():
    with MockIO('--autocomplete', '"app tests/autocomplete"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = set(mockio.stripped().splitlines())
        assert proposals == {'tests/autocomplete'}


def test_file_completer_subdir_content():
    with MockIO('--autocomplete', '"app tests/autocomplete/"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = mockio.stripped().splitlines()
        assert 'tests/autocomplete/__init__.py' in proposals

        assert 'tests/autocomplete/' not in proposals
        assert 'tests/autocomplete' not in proposals
        assert 'tests/__init__.py' not in proposals
        assert 'tests/' not in proposals
        assert '.gitignore' not in proposals
        assert '.' not in proposals
        assert '..' not in proposals


def test_file_completer_subdir_file():
    with MockIO('--autocomplete', '"app tests/autocomplete/__init__.py"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        assert mockio.stripped() == 'tests/autocomplete/__init__.py'


def test_file_completer_notexisting_dir():
    with MockIO('--autocomplete', '"app tests/there_is_no_dir/__init__.py"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        assert mockio.stripped() == ''


def test_complete_absolute_files():
    Path('/tmp/nuclear_test_autocomplete_425_896').write_text('')

    with MockIO('--autocomplete', '"app /tmp/nuclear_test_autocomplete_425"') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        assert mockio.stripped() == '/tmp/nuclear_test_autocomplete_425_896'

    Path('/tmp/nuclear_test_autocomplete_425_896').unlink()
