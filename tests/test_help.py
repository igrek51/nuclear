from .utils import *
from cliglue.processor import *
from cliglue.rule import *


def action_print_1():
    print('1')


def action_print_2():
    print('2')


def test_cli_arg_rule():
    assert CliArgRule(keywords='name', help='help',
                      syntax='syntaxSuffix').display_syntax_prefix() == 'name'
    assert CliArgRule(keywords=['name1', 'name2'], help='help',
                      syntax='syntaxSuffix').display_syntax_prefix() == 'name1, name2'
    assert CliArgRule(keywords=['name1', 'name2'], help='help',
                      syntax=None).display_syntax() == 'name1, name2'
    assert CliArgRule(keywords=['name1', 'name2'], help='help',
                      syntax='<suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CliArgRule(keywords=['name1', 'name2'], help='help',
                      syntax=' <suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CliArgRule(keywords=['name'], help='help', syntax=None).display_help(
        5) == 'name  - help'
    assert CliArgRule(keywords=['name'], help='help', syntax=None).display_help(3) == 'name - help'
    assert CliArgRule(keywords=['name'], help='help', syntax='<suffix>').display_help(
        3) == 'name <suffix> - help'
    assert CliArgRule(keywords=['name'], help='help', syntax='<s>').display_help(
        10) == 'name <s>   - help'


def test_args_test_help():
    def print_help(ap2):
        ap2.print_help()

    # basic execution with no args
    with MockIO(['help']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('help', print_help)
        ap.process()
        assert mockio.output_contains('Usage:')


def test_args_multilevel_commands_help():
    with MockIO(['--help']) as mockio:
        ap = ArgsProcessor('cmdline', '1.2.3')
        ap.add_param('global-param')
        ap.add_param('--global-param2', help='another parameter')
        ap.add_flag('--flag', help='a flag')
        ap_test = ap.add_subcommand('test')
        ap_test.add_param('test-param')
        ap_test_dupy = ap_test.add_subcommand('dupy', action=action_print_1)
        ap_test_dupy.add_param('z-parametrem', help='with param')
        ap_test.add_subcommand('audio', action=action_print_1, help='tests audio')
        ap_test_dupy.add_subcommand('2', action=action_print_2)
        ap.process()
        assert mockio.output_contains('Usage:')  # help
        assert mockio.output_contains('cmdline')
        assert mockio.output_contains('v1.2.3')
        assert mockio.output_contains('glue [options] <command>')
        assert mockio.output_contains('test --test-param <test-param>')
        assert mockio.output_contains('test dupy --z-parametrem <z-parametrem>')
        assert mockio.output_contains('test dupy 2')
        assert mockio.output_contains('test audio')
        assert mockio.output_contains('--global-param <global-param>')


def test_args_deafult_action_help():
    with MockIO(['--help']) as mockio:
        ap = ArgsProcessor('cmdline', '1.2.3', default_action=action_print_1, syntax=' <dupa> [optional]')
        ap.add_param('global-param')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
        assert mockio.assert_output_contains('glue [options] <dupa> [optional]')


def test_args_processor_description():
    with MockIO(['--help']) as mockio:
        ArgsProcessor(app_name='Appname', version='1.0.1', description='This is sample application').process()
        mockio.assert_output_contains('Appname v1.0.1\n')
        mockio.assert_output_contains('This is sample application')
