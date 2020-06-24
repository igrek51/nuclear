from nuclear import *
from tests.asserts import MockIO
from nuclear import __version__


def test_print_version():
    with MockIO('--version') as mockio:
        CliBuilder(version='1.2.3').run()
        assert mockio.stripped().startswith('v1.2.3')


def test_print_version_with_v():
    with MockIO('--version') as mockio:
        CliBuilder(version='v1.2.3').run()
        assert mockio.stripped().startswith('v1.2.3')


def test_print_name_with_version():
    with MockIO('--version') as mockio:
        CliBuilder(name='apk', version='v1.2.3').run()
        assert 'apk v1.2.3' in mockio.stripped()


def test_print_nuclear_version():
    with MockIO('--version') as mockio:
        CliBuilder(name='apk', version='1.2.3').run()
        assert f'apk v1.2.3 (nuclear v{__version__})' == mockio.stripped()


def test_print_nuclear_version_without_app_name():
    with MockIO('--version') as mockio:
        CliBuilder(version='1.2.3').run()
        assert f'v1.2.3 (nuclear v{__version__})' == mockio.stripped()
