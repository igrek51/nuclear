import re
import sys
from io import StringIO
from typing import Type
import logging

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

        # capture output from loggers
        self.logger = logging.getLogger('nuclear.sublog')
        self.old_handler, self.new_handler = None, None
        if self.logger.hasHandlers():
            self.old_handler = self.logger.handlers[0]
            self.new_handler = logging.StreamHandler(self.new_out)
            self.new_handler.setLevel(self.old_handler.level)
            self.new_handler.setFormatter(self.old_handler.formatter)

    def __enter__(self):
        self._mock_args.__enter__()
        sys.stdout, sys.stderr = self.new_out, self.new_err
        if self.old_handler is not None:
            self.logger.removeHandler(self.old_handler)
            self.logger.addHandler(self.new_handler)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._mock_args.__exit__(exc_type, exc_value, traceback)
        sys.stdout, sys.stderr = self.old_out, self.old_err
        sys.stdout.write(self.output())
        if self.old_handler is not None:
            self.logger.removeHandler(self.new_handler)
            self.logger.addHandler(self.old_handler)

    def output(self) -> str:
        return self.new_out.getvalue() + self.new_err.getvalue()

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


class StdoutCap:
    def __init__(self):
        # mock output
        self.new_out, self.new_err = StringIO(), StringIO()
        self.old_out, self.old_err = sys.stdout, sys.stderr

        # capture output from loggers
        self.logger = logging.getLogger('nuclear.sublog')
        self.old_handler, self.new_handler = None, None
        if self.logger.hasHandlers():
            self.old_handler = self.logger.handlers[0]
            self.new_handler = logging.StreamHandler(self.new_out)
            self.new_handler.setLevel(self.old_handler.level)
            self.new_handler.setFormatter(self.old_handler.formatter)

    def __enter__(self):
        sys.stdout, sys.stderr = self.new_out, self.new_err
        if self.old_handler is not None:
            self.logger.removeHandler(self.old_handler)
            self.logger.addHandler(self.new_handler)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout, sys.stderr = self.old_out, self.old_err
        sys.stdout.write(self.output())
        if self.old_handler is not None:
            self.logger.removeHandler(self.new_handler)
            self.logger.addHandler(self.old_handler)

    def output(self) -> str:
        return self.new_out.getvalue() + self.new_err.getvalue()

    def stripped(self) -> str:
        return self.output().strip()

    def uncolor(self) -> str:
        matcher = re.compile(r'\x1b\[[0-9]+(;[0-9]+)?m')
        return matcher.sub('', self.output())


def assert_multiline_match(text: str, regex_pattern: str):
    regex_lines = regex_pattern.strip().splitlines()
    text_lines = remove_ansi_sequences(text).strip().splitlines()

    if len(text_lines) < len(regex_lines):
        missing_lines = "\n".join(regex_lines[len(text_lines):])
        assert False, f'Actual text has {len(regex_lines) - len(text_lines)} less lines than a pattern.\nActual text:\n{text}'
    
    if len(text_lines) > len(regex_lines):
        extra_lines = "\n".join(text_lines[len(regex_lines):])
        assert False, f'Actual text has {len(text_lines) - len(regex_lines)} more lines than a pattern.\nActual text:\n{text}'

    for index, (regex_line, text_line) in enumerate(zip(regex_lines, text_lines)):
        match = re.fullmatch(regex_line, text_line)
        assert match, f'Actual Line #{index+1}:\n{text_line}\n does not match the Regex pattern:\n{regex_line}'


def remove_ansi_sequences(text: str) -> str:
    return re.sub(r'\x1b\[\d+(;\d+)?m', '', text)
