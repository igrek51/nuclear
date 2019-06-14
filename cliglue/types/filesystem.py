import os

from cliglue.parser.error import CliSyntaxError


def existing_file(arg: str) -> str:
    if not os.path.isfile(arg):
        raise CliSyntaxError('file does not exist: ' + arg)
    return arg


def existing_directory(arg: str) -> str:
    if not os.path.isdir(arg):
        raise CliSyntaxError('directory does not exist: ' + arg)
    return arg
