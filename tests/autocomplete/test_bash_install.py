from cliglue import *
from tests.asserts import MockIO, assert_error


def test_raw_install_without_permissions():
    with MockIO('--bash-install', 'dupa123') as mockio:
        cli = CliBuilder()
        assert_error(lambda: cli.run())
        assert 'root privileges' in mockio.output()
