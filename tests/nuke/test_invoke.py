import sys
from unittest.mock import MagicMock

from nuclear.nuke.invoke import parse_cli_args, depends, _execute_target, _executed_targets


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
