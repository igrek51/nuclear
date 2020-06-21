from cliglue import *
from cliglue.autocomplete.completers import file_completer
from tests.asserts import MockIO


def test_file_completer():
    with MockIO('--autocomplete', '"app "') as mockio:
        CliBuilder(reraise_error=True).has(
            arguments('f', choices=file_completer),
        ).run()
        proposals = mockio.stripped().splitlines()
        assert '.gitignore' in proposals
        assert 'tests/' in proposals
        assert 'tests/builder/' not in proposals
        assert 'tests/__init__.py' not in proposals
        assert '.' not in proposals
        assert '..' not in proposals
