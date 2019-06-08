from cliglue.processor import *
from .utils import *


def command1():
    print('None')


def action_dupa():
    print('dupa')


def command2(ap):
    param = ap.poll_next('param')
    print(param)
    return param


def command_poll_optional(ap):
    print(ap.poll_next())


def command_ap_typed(ap: ArgsProcessor):
    param = ap.poll_next()
    print(param)


def command3(ap):
    param = ap.peek_next()
    if not param:
        assert not ap.has_next()
    param2 = ap.poll_next()
    assert param == param2
    print(param)


def command4_remaining(ap):
    print(ap.poll_remaining_joined())


def commandpoll_remaining(ap):
    print(ap.poll_remaining())


def command5_poll(ap):
    while ap.has_next():
        print(ap.poll_next())


def command6_set_para(ap):
    para = ap.poll_next('para')
    ap.set_param('para', para)


def command_print_version_only(ap):
    ap.print_version()


def action_is_force(ap):
    print('force is: ' + str(ap.is_flag_set('force')))


def action_is_f(ap):
    print('force is: ' + str(ap.is_flag_set('f')))


def action_print_flag(ap):
    print(ap.is_flag_set('dup'))


def action_print_remaining(ap):
    print(ap.poll_remaining_joined())


def action_nothing():
    pass


def action_print_1():
    print('1')


def action_print_2():
    print('2')


def action_set_object_param(ap):
    ap.set_param('numberek', int(7))


def action_print_params(ap):
    print('param is: %s' % ap.get_param('param'))
    print('p is: %s' % ap.get_param('p'))


def action_print_param(ap):
    print(ap.get_param('param'))


def sample_processor1():
    ap = ArgsProcessor('appName', '1.0.1')
    ap.add_subcommand('command1', action=command1, help='help1')
    ap.add_subcommand(['command2', 'command22'], action=command2, help='help2', syntax='<param>')
    ap.add_subcommand(['command3', 'command33'], action=command3, help='help2', syntax='<param>')
    ap.add_subcommand('remain', action=command4_remaining, help='help4', syntax='<param>')
    ap.add_subcommand('poll', action=command5_poll, help='help5')
    ap.add_subcommand('--set-para', action=command6_set_para, help='set para')
    return ap


def test_args_simple_command():
    with MockIO(['du']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('du', action_dupa)
        ap.process()
        mockio.output_contains('dupa')


def test_subparser_version():
    def print_version(ap2):
        ap2.print_version()

    # basic execution with no args
    with MockIO(['version']) as mockio:
        ap = ArgsProcessor(version='2.1')
        ap.add_subcommand('version', print_version)
        ap.process()
        assert mockio.output_contains('2.1')


def test_argsprocessor_noarg():
    # basic execution with no args
    with MockIO([]) as mockio:
        ArgsProcessor('appName', '1.0.1').process()
        assert mockio.output_contains('Usage:')


def test_argsprocessor_bindings_setup():
    # test bindings setup
    sample_processor1()


def test_argsprocessor_bind_default_action():
    # test bindings
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_dupa)
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['-h']) as mockio:
        ap = ArgsProcessor(default_action=command1)
        ap.process()
        assert mockio.output_contains('Usage:')


def test_args_print_flag():
    # test processing params first
    with MockIO(['print-flag', '--dup']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-flag', action_print_flag)
        ap.add_flag('dup')
        ap.process()
        assert mockio.output_contains('True')
    with MockIO(['print-flag', '--d']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-flag', action_print_flag)
        ap.add_flag('dup')
        ap.process()
        assert mockio.output_contains('False')


def test_args_no_next_arg():
    # test lack of next argument
    with MockIO(['command2']) as mockio:
        sample_processor1().process()
        assert 'ERROR' in mockio.output()
        assert 'no required argument "param" given' in mockio.output()
    with MockIO(['command33']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'None\n'


def test_argsprocessor_binding():
    # test binding with no argProcessor
    with MockIO(['command1']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'None\n'


def test_argsprocessor_poll_remaining_joined():
    # test pollRemainingJoined():
    with MockIO(['remain']) as mockio:
        sample_processor1().process()
        assert mockio.output() == '\n'
    with MockIO(['remain', '1']) as mockio:
        sample_processor1().process()
        assert mockio.output_strip() == '1'
    with MockIO(['remain', '1', 'abc', 'd']) as mockio:
        sample_processor1().process()
        assert mockio.output_strip() == '1 abc d'


def test_argsprocessor_poll_remaining():
    with MockIO(['remaining', 'jasna', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=commandpoll_remaining)
        ap.process()
        assert mockio.output_strip() == "['remaining', 'jasna', 'dupa']"


def test_args_poll():
    # test polling
    with MockIO(['poll', '123', '456', '789']) as mockio:
        sample_processor1().process()
        assert mockio.output() == '123\n456\n789\n'


def test_args_removing_args():
    # test removing parameters
    with MockIO(['remain', 'jasna', '--to-remove', 'dupa', 'dupaa', '--flagg', 'abc', '1']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('--to-remove')
        ap.add_flag('--flagg')
        ap.add_subcommand('remain', action_print_remaining)
        ap.process()
        assert mockio.output() == 'jasna dupaa abc 1\n'


def test_args_unknown_arg():
    # test unknown argument
    with MockIO(['jasna', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_nothing)
        ap.process()
        assert 'invalid arguments: jasna dupa' in mockio.output()


def test_args_default_action():
    def print_help(ap2):
        ap2.print_help()

    with MockIO(['dupa']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command2)
        ap.process()
        assert mockio.output() == 'dupa\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command_poll_optional)
        ap.process()
        assert mockio.output() == 'None\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=print_help)
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
    # test getting params
    with MockIO(['dupa2']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command2)
        ap.process()
        assert mockio.output() == 'dupa2\n'
    with MockIO([]) as mockio:
        ArgsProcessor(default_action=action_print_1).process()
        assert mockio.output_contains('1')
    # default action - help
    with MockIO([]) as mockio:
        ap = ArgsProcessor()
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
    # default action - help
    with MockIO(['print2']) as mockio:
        ap = ArgsProcessor(default_action=action_print_1)
        ap.add_subcommand('print2', action=action_print_2)
        ap.process()
        assert mockio.output_contains('2')
        assert not mockio.output_contains('1')


def test_args_bind_default_options():
    with MockIO(['-v']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output() == 'appName v1.0.1\n'
    with MockIO(['-v', '-v']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output_contains('appName v1.0.1\n')
        assert mockio.output_contains('invalid arguments')
    with MockIO(['-h']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def test_args_object_params():
    with MockIO([]):
        ap = ArgsProcessor(default_action=action_set_object_param)
        ap.process()
        assert not ap.is_param('dupa')
        assert ap.get_param('dupa') is None
        assert ap.is_param('numberek')
        assert ap.get_param('numberek') is 7


def test_args_options_and_default_acction():
    with MockIO(['-v2', '-v2']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command1)
        ap.add_subcommand('command1', command1, help='help1')
        ap.process()
        assert mockio.output_contains('None')
        assert mockio.output_contains('invalid arguments')
        assert mockio.output_contains('v2')


def test_args_toomanyargs():
    with MockIO(['command1', 'two', 'much']) as mockio:
        sample_processor1().process()
        assert 'None' in mockio.output()
        assert 'invalid arguments: two much' in mockio.output()


def test_argsprocessor_bind_flag():
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('force').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['--force']) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('force').process()
        assert mockio.output() == 'force is: True\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('force', '--for').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['--for']) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('force', '--for').process()
        assert mockio.output() == 'force is: True\n'
    # single letter
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('f').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['-f']) as mockio:
        ap = ArgsProcessor(default_action=action_is_f)
        ap.add_flag('f').process()
        assert mockio.output() == 'force is: True\n'
    with MockIO(['-f']) as mockio:
        ap = ArgsProcessor(default_action=action_is_force)
        ap.add_flag('force', ['-f', '--force']).process()
        assert mockio.output() == 'force is: True\n'


def test_args_add_empty_command():
    with MockIO(['test']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def test_args_default_aciton_with_flags():
    with MockIO(['--flag']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_flag('flag')
        ap.process()
        assert mockio.output().strip() == 'None'


def test_args_python3_command():
    # basic execution with no args
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.process()
        assert mockio.output() == 'None\n'


def test_ap_strong_typed():
    with MockIO(['param']) as mockio:
        ArgsProcessor(default_action=command_ap_typed).process()
        mockio.assert_output_contains('param')
