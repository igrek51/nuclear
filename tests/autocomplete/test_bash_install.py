from cliglue import *
from tests.asserts import MockIO, assert_error


def test_bash_install_without_permissions():
    with MockIO('--install-bash', 'test_dupa123') as mockio:
        cli = CliBuilder()
        assert_error(lambda: cli.run())
        assert 'root privileges' in mockio.output()


def test_autocomplete_install_without_permissions():
    with MockIO('--install-autocomplete', 'test_dupa123') as mockio:
        cli = CliBuilder()
        assert_error(lambda: cli.run())
        assert 'root privileges' in mockio.output()
