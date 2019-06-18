import sys
from io import StringIO

import mock

from cliglue.parser.error import CliError


def assert_error(action, expected_error=None):
    try:
        action()
        assert False
    except RuntimeError as e:
        if expected_error:
            assert expected_error in str(e)


def assert_cli_error(action, expected_error=None):
    try:
        action()
        assert False
    except CliError as e:
        if expected_error:
            assert expected_error in str(e)


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

    def output_contains(self, in_str):
        return in_str in self.output()

    def assert_output_contains(self, in_str):
        assert in_str in self.output()
        return True

    def assert_output(self, in_str):
        assert in_str == self.output()
        return True
