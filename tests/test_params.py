from .utils import *
from cliglue.processor import *


def action_print_param1(ap):
    print(ap.get_param('param'))


def command2(ap):
    param = ap.poll_next('param')
    print(param)
    return param


def action_print_params(ap):
    print('param is: %s' % ap.get_param('param'))
    print('p is: %s' % ap.get_param('p'))


def action_print_from_to(ap):
    print('range: ' + ap.get_param('fromDate') + ' - ' + ap.get_param('toDate'))


def action_get_param(ap):
    print(ap.get_param('musthave', required=True))


def action_print_param(ap):
    print(ap.get_param('param'))


def sample_processor1():
    ap = ArgsProcessor('appName', '1.0.1')
    ap.add_subcommand(['command2', 'command22'], action=command2, help='help2', syntax='<param>')
    return ap


def test_args_params_first():
    # test processing params first
    with MockIO(['print-param', '--param=dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('dupa')
    with MockIO(['print-param', '--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('dupa')
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def test_argsprocessor_given_param():
    with MockIO(['command2', 'dupa']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'dupa\n'


def action_test_args_params_with_hyphens(ap):
    print(ap.get_param('--param-one'))
    print(ap.get_param('param-one'))
    print(ap.get_param('param2'))
    print(ap.get_param('--param2'))
    print(ap.get_param('p'))


def test_args_params_with_hyphens():
    with MockIO(['--param-one', 'value-one', '--param2', 'p2', '-p', 'p3']) as mockio:
        ap = ArgsProcessor(default_action=action_test_args_params_with_hyphens)
        ap.add_param('--param-one')
        ap.add_param('param2')
        ap.add_param('p')
        ap.process()
        assert mockio.output() == 'value-one\nvalue-one\np2\np2\np3\n'


def test_args_add_param():
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', help='set param').process()
        assert 'param is: None\n' in mockio.output()
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', help='set param').process()
        assert 'param is: dupa\n' in mockio.output()
    with MockIO(['--parameter', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', keywords='--parameter', help='set param').process()
        assert 'param is: dupa\n' in mockio.output()
    # single letter
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('p', help='set param').process()
        assert 'p is: None\n' in mockio.output()
    with MockIO(['-p', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('p', help='set param').process()
        assert 'p is: dupa\n' in mockio.output()


def test_argsprocessor_2params():
    with MockIO(['print', '--from', 'today', '--to', 'tomorrow']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.add_param('fromDate', keywords='--from')
        ap.add_param('toDate', keywords='--to')
        ap.add_subcommand('print', action_print_from_to)
        ap.process()
        assert 'range: today - tomorrow' in mockio.output()


def test_args_get_missing_required_param():
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=action_get_param)
        ap.add_param('musthave')
        ap.process()
        assert 'no required param given: musthave' in mockio.output()


def test_args_multilevel_params():
    with MockIO(['test', 'dupy', '--param=dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test').add_subcommand('dupy', action=action_print_param).add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['test', 'dupy', '--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test').add_subcommand('dupy', action=action_print_param).add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'


def test_args_default_aciton_with_params():
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'


def test_args_empty_param():
    with MockIO(['--param']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('no required argument "--param" given')


def test_args_required_param():
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['--none']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('None')
        assert mockio.output_contains('invalid arguments')
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param', required=True)
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['--none']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param', required=True)
        ap.process()
        assert mockio.output_contains('missing params are required: --param')
