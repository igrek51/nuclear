from utils.shell import *
from .utils import *


def test_output():
    with MockIO() as mockio:
        debug('message')
        assert mockio.output_contains('message')
        assert mockio.output_contains('debug')
        info('message')
        assert mockio.output_contains('info')
        warn('message')
        assert mockio.output_contains('warn')
        error('message')
        assert mockio.output_contains('ERROR')
        info(7)
        assert mockio.output_contains('7')


def test_fatal():
    assert_error(lambda: fatal('fatality'))
    assert_error(lambda: fatal('fatality'), 'fatality')


def test_shell_exec():
    shell('echo test')
    assert_error(lambda: shell('dupafatality'))
    assert shell_error_code('echo test') == 0
    assert shell_output('echo test') == 'test\n'
    assert shell_output('echo żółć') == u'żółć\n'
    assert shell_output('echo test', as_bytes=True) == b'test\n'
    assert shell_output('echo test', as_bytes=True) == 'test\n'.encode('utf-8')
    assert shell_output('echo test', as_bytes=True).decode('utf-8') == 'test\n'


def test_script_real_dir():
    real_dir_expected = os.path.join(os.getcwd(), 'cli_glue')
    assert script_real_dir() == real_dir_expected


def test_script_real_path():
    assert '/pytest.py' in script_real_path()
