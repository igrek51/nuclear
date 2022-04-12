from pathlib import Path

from nuclear import shell, shell_error_code, shell_output, CommandError
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


def test_old_import_style():
    from nuclear.utils.shell import shell_output
    assert shell_output('echo test') == 'test\n'


def test_shell_error_code():
    assert shell_error_code('shiiiiit') != 0
    try:
        shell('shiiiiit')
    except CommandError as e:
        assert e.cmd == 'shiiiiit'
        assert e.return_code != 0
        assert 'command error: shiiiiit: ' in str(e)


def test_write_stdout_to_file():
    tmpfile = Path('/tmp/nuclear_test_write_stdout_to_file')
    if tmpfile.is_file():
        tmpfile.unlink()

    shell('echo "test stdout"', output_file=tmpfile)
    assert tmpfile.read_text() == 'test stdout\n'

    tmpfile.unlink()