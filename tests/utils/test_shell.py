from pathlib import Path
import time

import backoff

from nuclear import shell, shell_error_code, shell_output, CommandError
from nuclear.shell import BackgroundCommand
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
    live_lines = []

    cmd = BackgroundCommand(
        'while sleep 0.1; do echo 1; done', 
        debug=True,
        print_stdout=True,
        on_next_line=lambda line: live_lines.append(line),
    )
    assert cmd.is_running

    @backoff.on_exception(backoff.expo, AssertionError, factor=0.1, max_value=0.5, max_time=5, jitter=None)
    def check():
        assert '1\n1\n' in cmd.stdout
        assert '1\n' in live_lines
    check()

    cmd.terminate()
    assert not cmd.is_running
    assert '1\n1\n' in cmd.stdout


def test_background_long_command_without_output():
    test_start = time.time()
    cmd = BackgroundCommand('sleep 10', debug=True, shell=False)
    assert cmd.is_running
    cmd.terminate()
    cmd.terminate()
    assert not cmd.is_running
    assert time.time() - test_start <= 9, 'test took too long'


def test_background_long_shell_command_without_output():
    test_start = time.time()
    cmd = BackgroundCommand('echo running && sleep 10', debug=True, shell=True)
    assert cmd.is_running
    
    @backoff.on_exception(backoff.expo, AssertionError, factor=0.1, max_value=0.5, max_time=5, jitter=None)
    def check():
        assert cmd.stdout == 'running\n'
    check()

    cmd.terminate()
    cmd.terminate()
    assert not cmd.is_running
    assert time.time() - test_start <= 9, 'test took too long'


def test_background_command_failed():
    error = None

    def on_error(e: CommandError):
        nonlocal error
        error = e

    cmd = BackgroundCommand('shiiiiit', on_error=on_error)
    cmd.wait()
    assert not cmd.is_running
    assert 'command error: shiiiiit' in str(error)
