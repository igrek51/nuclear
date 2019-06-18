from cliglue.utils.shell import shell, shell_error_code, shell_output
from tests.asserts import assert_error


def test_shell_exec():
    shell('echo test')
    assert_error(lambda: shell('no-faking-command'))
    assert shell_error_code('echo test') == 0
    assert shell_output('echo test') == 'test\n'
    assert shell_output('echo żółć') == u'żółć\n'
    assert shell_output('echo test', as_bytes=True) == b'test\n'
    assert shell_output('echo test', as_bytes=True) == 'test\n'.encode('utf-8')
    assert shell_output('echo test', as_bytes=True).decode('utf-8') == 'test\n'
