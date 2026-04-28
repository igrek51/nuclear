import sys
from unittest.mock import MagicMock, patch

from nuclear.nuke.invoke import parse_cli_args, depends, _execute_target, _executed_targets, _list_target_names


def test_depends_decorator():
    """Test that depends decorator sets __depends__ attribute."""
    @depends('build')
    def test():
        pass

    assert hasattr(test, '__depends__')
    assert test.__depends__ == ('build',)


def test_depends_multiple():
    """Test depends decorator with multiple dependencies."""
    @depends('build', 'lint')
    def deploy():
        pass

    assert deploy.__depends__ == ('build', 'lint')


def test_execute_target_with_dependencies():
    """Test that dependencies are executed before target."""
    execution_order = []

    def build():
        execution_order.append('build')

    def test_func():
        execution_order.append('test')

    test_func.__depends__ = ('build',)

    main_module = MagicMock()
    main_module.__name__ = 'test_module'
    main_module.build = build
    main_module.test = test_func

    _executed_targets.clear()
    _execute_target(main_module, 'test')

    assert execution_order == ['build', 'test']


def test_execute_target_dependency_called_once():
    """Test that shared dependencies are executed only once."""
    execution_order = []

    def build():
        execution_order.append('build')

    def test_func():
        execution_order.append('test')

    def deploy():
        execution_order.append('deploy')

    test_func.__depends__ = ('build',)
    deploy.__depends__ = ('build',)

    main_module = MagicMock()
    main_module.__name__ = 'test_module'
    main_module.build = build
    main_module.test = test_func
    main_module.deploy = deploy

    _executed_targets.clear()
    _execute_target(main_module, 'test')
    _execute_target(main_module, 'deploy')

    # build should only be called once
    assert execution_order.count('build') == 1
    assert execution_order == ['build', 'test', 'deploy']


def test_execute_target_already_executed():
    """Test that already executed targets are skipped."""
    execution_order = []

    def build():
        execution_order.append('build')

    main_module = MagicMock()
    main_module.__name__ = 'test_module'
    main_module.build = build

    _executed_targets.clear()
    _execute_target(main_module, 'build')
    _execute_target(main_module, 'build')

    # build should only be called once
    assert execution_order == ['build']


def test_parse_cli_args():
    positional, overrides = parse_cli_args(['--name=value', 'pos1', '--flag', 'pos2', '--long-name="long value"'])
    assert positional == ['pos1', 'pos2']
    assert overrides == {
        'name': 'value',
        'flag': '1',
        'long_name': 'long value',
    }


def test_parse_cli_args_kebab_case():
    positional, overrides = parse_cli_args(['--kebab-case=value', '--another-flag'])
    assert positional == []
    assert overrides == {
        'kebab_case': 'value',
        'another_flag': '1',
    }


def test_parse_cli_args_empty():
    positional, overrides = parse_cli_args([])
    assert positional == []
    assert overrides == {}


def test_parse_cli_args_only_positional():
    positional, overrides = parse_cli_args(['pos1', 'pos2'])
    assert positional == ['pos1', 'pos2']
    assert overrides == {}


def test_list_target_names_excludes_imported_functions():
    """Test that imported functions (e.g. Unidecode) are not listed as targets."""
    def local_action():
        pass
    local_action.__module__ = 'nukefile'

    def imported_func():
        pass
    imported_func.__module__ = 'unidecode'  # simulates: from unidecode import unidecode

    mock_module = MagicMock()
    mock_module.__name__ = 'nukefile'
    mock_module.__dir__ = lambda self: ['local_action', 'imported_func']
    mock_module.local_action = local_action
    mock_module.imported_func = imported_func

    with patch.dict(sys.modules, {'__main__': mock_module}):
        targets = _list_target_names()

    assert 'local_action' in targets
    assert 'imported_func' not in targets


def test_list_target_names_excludes_private_functions():
    """Test that private functions (starting with _) are not listed as targets."""
    def public_action():
        pass
    public_action.__module__ = 'nukefile'

    def _private_action():
        pass
    _private_action.__module__ = 'nukefile'

    mock_module = MagicMock()
    mock_module.__name__ = 'nukefile'
    mock_module.__dir__ = lambda self: ['public_action', '_private_action']
    mock_module.public_action = public_action
    mock_module._private_action = _private_action

    with patch.dict(sys.modules, {'__main__': mock_module}):
        targets = _list_target_names()

    assert 'public_action' in targets
    assert '_private_action' not in targets


def test_list_target_names_excludes_non_function_callables():
    """Test that callable classes imported from other modules are not listed as targets."""
    def local_action():
        pass
    local_action.__module__ = 'nukefile'

    class CallableClass:
        def __call__(self):
            pass

    imported_callable = CallableClass()

    mock_module = MagicMock()
    mock_module.__name__ = 'nukefile'
    mock_module.__dir__ = lambda self: ['local_action', 'imported_callable']
    mock_module.local_action = local_action
    mock_module.imported_callable = imported_callable

    with patch.dict(sys.modules, {'__main__': mock_module}):
        targets = _list_target_names()

    assert 'local_action' in targets
    assert 'imported_callable' not in targets
