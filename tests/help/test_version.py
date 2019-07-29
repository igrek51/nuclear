from cliglue import *
from tests.asserts import MockIO


def test_print_version():
    with MockIO('--version') as mockio:
        CliBuilder(version='1.2.3').run()
        assert 'v1.2.3' == mockio.stripped()


def test_print_version_with_v():
    with MockIO('--version') as mockio:
        CliBuilder(version='v1.2.3').run()
        assert 'v1.2.3' == mockio.stripped()
