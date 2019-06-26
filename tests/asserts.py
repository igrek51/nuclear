import sys
from io import StringIO
from typing import Type

import mock

from cliglue.parser.error import CliError


def assert_error(action, error_type: Type[Exception] = RuntimeError, expected_msg: str = None):
    try:
        action()
        assert False
    except error_type as e:
        assert isinstance(e, error_type)
        if expected_msg:
            assert expected_msg in str(e)


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

    def output(self):
        return self.new_out.getvalue()

    def stripped_output(self):
        return self.output().strip()
