import re
import sys
from io import StringIO
from typing import Type

import mock

from nuclear.parser.error import CliError


def assert_error(action, error_type: Type[Exception] = RuntimeError, expected_msg: str = None):
    try:
        action()
        assert False, 'should raise error'
    except error_type as e:
        assert isinstance(e, error_type)
        if expected_msg:
            assert expected_msg in str(e), 'unexpected error message'


def assert_cli_error(action, expected_error: str = None):
    assert_error(action, CliError, expected_error)


def assert_system_exit(action):
    try:
        action()
        assert False
    except SystemExit as e:
        # exit with error code 0
        assert str(e) == '0'


class MockIO:
    def __init__(self, *in_args: str):
        # mock cli input
        self._mock_args = mock.patch.object(sys, 'argv', ['glue'] + list(in_args))
        # mock output
        self.new_out, self.new_err = StringIO(), StringIO()
        self.old_out, self.old_err = sys.stdout, sys.stderr

    def __enter__(self):
        self._mock_args.__enter__()
        sys.stdout, sys.stderr = self.new_out, self.new_err
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._mock_args.__exit__(exc_type, exc_value, traceback)
        sys.stdout, sys.stderr = self.old_out, self.old_err
        sys.stdout.write(self.output())

    def output(self) -> str:
        return self.new_out.getvalue()

    def stripped(self) -> str:
        return self.output().strip()

    def uncolor(self) -> str:
        matcher = re.compile(r'\x1b\[[0-9]+(;[0-9]+)?m')
        return matcher.sub('', self.output())

    def assert_match(self, regex: str):
        matcher = re.compile(regex)
        for line in self.output().splitlines():
            if matcher.search(line):
                return
        assert False, f'Regex: "{regex}" does not match the output: {self.output()}'

    def assert_match_uncolor(self, regex: str):
        matcher = re.compile(regex)
        for line in self.uncolor().splitlines():
            if matcher.search(line):
                return
        assert False, f'Regex: "{regex}" does not match the output: {self.uncolor()}'

    def assert_not_match(self, regex: str):
        matcher = re.compile(regex)
        for line in self.output().splitlines():
            if matcher.search(line):
                assert False, f'Regex: "{regex}" should not match the output: {self.output()}'
