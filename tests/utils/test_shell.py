from pathlib import Path
import time

from nuclear import shell, shell_error_code, shell_output, CommandError
from nuclear.shell.shell_utils import BackgroundCommand
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


def test_background_command():
    cmd = BackgroundCommand(
        'while sleep 0.1; do echo 1; done', 
        debug=True, 
        print_stdout=True, 
        on_next_line=lambda line: print(line*2),
    )
    assert cmd.is_running
    time.sleep(0.2)
    assert '1' in cmd.stdout
    cmd.terminate()
    assert not cmd.is_running
    assert '1' in cmd.stdout


def test_background_command_long_command_without_output():
    cmd = BackgroundCommand('sleep 10', debug=True)
    assert cmd.is_running
    time.sleep(0.5)
    cmd.terminate()
    assert not cmd.is_running


def test_background_command_failed():
    error = None
    
    def on_error(e: CommandError):
        nonlocal error
        error = e

    cmd = BackgroundCommand('shiiiiit', on_error=on_error)
    cmd.wait()
    assert not cmd.is_running
    assert 'command error: shiiiiit' in str(error)
