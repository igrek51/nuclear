from cliglue.processor import *
from tests.utils import *


def action_test_args_poll_from_subcommand(ap):
    print(ap.poll_remaining_joined())


def completer_screen1():
    return ['HDMI', 'eDP']


def completer_screen_with_ap(ap):
    return ['HDMI', 'eDP'] + ap.poll_remaining()


def test_args_poll_from_subcommand():
    with MockIO(['--autocomplete-install2', 'jasna', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('--autocomplete-install2', action=action_test_args_poll_from_subcommand)
        ap.process()
        assert mockio.output_strip() == 'jasna dupa'


def test_args_bash_install_permissions():
    with MockIO(['--bash-install', 'dupa']):
        assert_ap_error(ArgsProcessor(), 'failed executing')


def test_args_autocomplete():
    with MockIO(['--bash-autocomplete', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        assert mockio.output() == '\n'


def test_args_autocomplete_first_list():
    with MockIO(['--bash-autocomplete', 'dupa ']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        mockio.assert_output_contains('-h\n')
        mockio.assert_output_contains('--help\n')
        mockio.assert_output_contains('-v\n')
        mockio.assert_output_contains('--version\n')
        mockio.assert_output_contains('--bash-install\n')
        mockio.assert_output_contains('--bash-autocomplete\n')
    with MockIO(['--bash-autocomplete', '"dupa "']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        mockio.assert_output_contains('--help\n')


def test_args_autocomplete_command_flag_param():
    with MockIO(['--bash-autocomplete', 'dupa ']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('command')
        ap.add_flag('flag1')
        ap.add_flag('--flag2')
        ap.add_param('param1')
        ap.add_param('--param2')
        ap.process()
        mockio.assert_output_contains('command\n')
        mockio.assert_output_contains('--flag1\n')
        mockio.assert_output_contains('--flag2\n')
        mockio.assert_output_contains('--param1\n')
        mockio.assert_output_contains('--param2\n')


def test_args_autocomplete_subcommand():
    with MockIO(['--bash-autocomplete', 'dupa command ']) as mockio:
        ap = ArgsProcessor()
        ap_command = ap.add_subcommand('command')
        ap_command.add_subcommand('sub2')
        ap_command.add_flag('flag1')
        ap_command.add_param('param1')
        ap.process()
        assert 'command' not in mockio.output()
        mockio.assert_output_contains('sub2\n')
        mockio.assert_output_contains('--flag1\n')
        mockio.assert_output_contains('--param1\n')
    with MockIO(['--bash-autocomplete', 'dupa com']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('command')
        ap.process()
        mockio.assert_output('command\n')
    with MockIO(['--bash-autocomplete', 'dupa c1 c2 ']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('c1').add_subcommand('c2').add_subcommand('c3')
        ap.process()
        assert not mockio.output_contains('c1')
        assert not mockio.output_contains('c2')
        mockio.assert_output_contains('c3\n')
        assert not mockio.output_contains('--help')


def test_args_autocomplete_params():
    with MockIO(['--bash-autocomplete', 'dupa --param ']) as mockio:
        ap = ArgsProcessor().add_param('param', choices=['jasna', 'dupa'])
        ap.process()
        mockio.assert_output_contains('jasna\ndupa\n')
    with MockIO(['--bash-autocomplete', 'dupa --param=']) as mockio:
        ap = ArgsProcessor().add_param('param', choices=['jasna', 'dupa'])
        ap.process()
        mockio.assert_output('jasna\ndupa\n')


def test_args_autocomplete_params_choices():
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME --screen ']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_param('screen', choices=['HDMI', 'eDP'])
        ap.process()
        mockio.assert_output_contains('HDMI\neDP\n')
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME --screen=']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_param('screen', choices=completer_screen1)
        ap.process()
        mockio.assert_output('HDMI\neDP\n')
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME --screen=']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_param('screen', choices=completer_screen_with_ap)
        ap.process()
        mockio.assert_output('HDMI\neDP\n')


def test_args_autocomplete_command_choices():
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME screen ']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_subcommand('screen', choices=['HDMI', 'eDP'])
        ap.process()
        mockio.assert_output_contains('HDMI\neDP\n')
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME screen ']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_subcommand('screen', choices=completer_screen1)
        ap.process()
        mockio.assert_output_contains('HDMI\neDP\n')
    with MockIO(['--bash-autocomplete', 'dupa --new AWSME screen ']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('new')
        ap.add_subcommand('screen', choices=completer_screen_with_ap)
        ap.process()
        mockio.assert_output_contains('HDMI\neDP\n')


def test_args_autocomplete_command_last_word_space():
    with MockIO(['--bash-autocomplete', 'lichking info age']) as mockio:
        ap = ArgsProcessor()
        ap_info = ap.add_subcommand('info')
        ap_info.add_subcommand('age')
        ap.process()
        mockio.assert_output_contains('age\n')
