import os

from cliglue.parser.error import ArgumentSyntaxError


def existing_file(arg: str) -> str:
    if not os.path.isfile(arg):
        raise ArgumentSyntaxError('file does not exist: ' + arg)
    return arg


def existing_directory(arg: str) -> str:
    if not os.path.isdir(arg):
        raise ArgumentSyntaxError('directory does not exist: ' + arg)
    return arg
