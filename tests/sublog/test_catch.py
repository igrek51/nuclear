from nuclear import CliBuilder
from nuclear.sublog import add_context, error_handler, log_exception
from tests.asserts import MockIO
import importlib.util


def test_sublog_traceback():
    with MockIO() as mockio:
        with error_handler():
            with add_context('initializing', request_id=42):
                with add_context('liftoff', speed='zero'):
                    disaster()

        mockio.assert_match_uncolor('ERROR initializing: liftoff: disaster, request_id=42 speed=zero '
                                    'cause=RuntimeError '
                                    'traceback="(.+)/test_catch.py:12, '
                                    '(.+)/test_catch.py:22, '
                                    '(.+)/test_catch.py:26"?$')


def disaster():
    reason()


def reason():
    raise RuntimeError('disaster')


def test_keyboard_interrupt():
    with MockIO() as mockio:
        try:
            with error_handler():
                raise KeyboardInterrupt()
            assert False, 'should exit'
        except SystemExit as e:
            assert str(e) == '1', 'should exit with error code 1'

        assert 'KeyboardInterrupt' in mockio.output()


def test_catch_with_context_name():
    with MockIO() as mockio:
        with error_handler('hacking time'):
            raise RuntimeError('nope')

        mockio.assert_match_uncolor('ERROR hacking time: nope, '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_catch.py:44"?$')


def test_catch_chained_exception_cause():
    with MockIO() as mockio:
        with error_handler('hacking time'):
            try:
                raise AttributeError('real cause')
            except AttributeError as e:
                raise RuntimeError('wrapper') from e

        mockio.assert_match_uncolor('ERROR hacking time: wrapper: real cause, '
                                    'cause=AttributeError '
                                    'traceback=(.+)/test_catch.py:55"?$')


def test_recover_from_dynamically_imported_module():
    with MockIO() as mockio:
        with error_handler('hacking time'):

            spec = importlib.util.spec_from_file_location("dynamic", 'tests/sublog/res/dynamic.py')
            ext_module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            assert loader is not None, 'no module loader'
            loader.exec_module(ext_module)

        mockio.assert_match_uncolor(r'ERROR hacking time: Fire!, '
                                    r'cause=RuntimeError '
                                    r'traceback="(.+)/test_catch.py:72, '
                                    r'<frozen importlib._bootstrap_external>:\d+, '
                                    r'<frozen importlib._bootstrap>:\d+, '
                                    r'(.+)/dynamic.py:1"$')


def test_catch_and_log_exception_from_builder():
    with MockIO() as mockio:
        def doit():
            raise RuntimeError('fail')

        cli = CliBuilder(log_error=True, run=doit)
        cli.run()

        mockio.assert_match_uncolor('ERROR fail, '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_catch.py:85"?$')


def test_log_exception():
    with MockIO() as mockio:
        try:
            raise RuntimeError('fail')
        except Exception as e:
            log_exception(e)

        mockio.assert_match_uncolor('ERROR fail, '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_catch.py:98"?$')
