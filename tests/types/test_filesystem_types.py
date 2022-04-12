from pathlib import Path
from nuclear import *
from nuclear.types.filesystem import existing_file, existing_directory
from tests.asserts import MockIO, assert_cli_error


def test_not_existing_file():
    with MockIO('--file', '/dupa'):
        cli = CliBuilder(usage_onerror=False, reraise_error=True).has(
            parameter('file', type=existing_file),
        )
        assert_cli_error(lambda: cli.run())


def test_existing_file():
    script_file = Path('tests/types/__init__.py').as_posix()
    with MockIO('--file', script_file):
        CliBuilder(usage_onerror=False, reraise_error=True).has(
            parameter('file', type=existing_file),
        ).run()


def test_not_existing_dir():
    with MockIO('--dir', '/dupa'):
        cli = CliBuilder(usage_onerror=False, reraise_error=True).has(
            parameter('dir', type=existing_directory),
        )
        assert_cli_error(lambda: cli.run())


def test_file_as_dir():
    script_file = Path('tests/types/__init__.py').as_posix()
    with MockIO('--dir', script_file):
        cli = CliBuilder(usage_onerror=False, reraise_error=True).has(
            parameter('dir', type=existing_directory),
        )
        assert_cli_error(lambda: cli.run())


def test_existing_dir():
    script_dir = Path('tests/types').as_posix()
    with MockIO('--dir', script_dir):
        CliBuilder(usage_onerror=False, reraise_error=True).has(
            parameter('dir', type=existing_directory),
        ).run()
