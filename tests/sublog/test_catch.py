from nuclear.sublog import wrap_context, logerr
from tests.asserts import MockIO
import importlib.util


def test_sublog_traceback():
    with MockIO() as mockio:
        with logerr():
            with wrap_context('initializing', request_id=42):
                with wrap_context('liftoff', speed='zero'):
                    disaster()

        mockio.assert_match_uncolor('ERROR initializing: liftoff: disaster request_id=42 speed=zero '
                                    'cause=RuntimeError '
                                    'traceback="(.+)/test_catch.py:11, '
                                    '(.+)/test_catch.py:21, '
                                    '(.+)/test_catch.py:25"$')


def disaster():
    reason()


def reason():
    raise RuntimeError('disaster')


def test_keyboard_interrupt():
    with MockIO() as mockio:
        try:
            with logerr():
                raise KeyboardInterrupt()
            assert False, 'should exit'
        except SystemExit as e:
            assert str(e) == '1', 'should exit with error code 1'

        assert 'KeyboardInterrupt' in mockio.output()


def test_catch_with_context_name():
    with MockIO() as mockio:
        with logerr('hacking time'):
            raise RuntimeError('nope')

        mockio.assert_match_uncolor('ERROR hacking time: nope '
                                    'cause=RuntimeError '
                                    'traceback=(.+)/test_catch.py:43$')


def test_catch_chained_exception_cause():
    with MockIO() as mockio:
        with logerr('hacking time'):
            try:
                raise AttributeError('real cause')
            except AttributeError as e:
                raise RuntimeError('wrapper') from e

        mockio.assert_match_uncolor('ERROR hacking time: wrapper: real cause '
                                    'cause=AttributeError '
                                    'traceback=(.+)/test_catch.py:54$')


def test_recover_from_dynamically_imported_module():
    with MockIO() as mockio:
        with logerr('hacking time'):

            spec = importlib.util.spec_from_file_location("dynamic", 'tests/sublog/res/dynamic.py')
            ext_module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            assert loader is not None, 'no module loader'
            loader.exec_module(ext_module)

        mockio.assert_match_uncolor(r'ERROR hacking time: Fire! '
                                    r'cause=RuntimeError '
                                    r'traceback="(.+)/test_catch.py:71, '
                                    r'<frozen importlib._bootstrap_external>:\d+, '
                                    r'<frozen importlib._bootstrap>:\d+, '
                                    r'(.+)/dynamic.py:1"$')
