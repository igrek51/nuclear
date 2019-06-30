from cliglue import *
from tests.asserts import MockIO, assert_cli_error
from tests.parser.actions import *


def test_param_with_2_args():
    with MockIO('--param', 'OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('-p', 'OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_param_with_2_args_with_action():
    with MockIO('run', '--param', 'OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('run', '-p', 'OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param', 'p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_set_param_with_equals():
    with MockIO('run', '--param=OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('run', '-p=OK') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_param),
            parameter('param', 'p'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('--param=OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param'),
        ).run()
        assert mockio.output() == 'param: OK\n'
    with MockIO('-p=OK') as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: OK\n'


def test_no_param():
    with MockIO() as mockio:
        CliBuilder(run=print_param).has(
            parameter('--param', '-p'),
        ).run()
        assert mockio.output() == 'param: None\n'


def test_int_type_param():
    def print_param_and_type(param):
        print(f'param: {param}, type: {type(param).__name__}')

    with MockIO('--param', '42') as mockio:
        CliBuilder(run=print_param_and_type).has(
            parameter('--param', type=int),
        ).run()
        assert mockio.output() == 'param: 42, type: int\n'


def test_missing_required_param():
    with MockIO():
        cli = CliBuilder(run=print_param, help_onerror=False, reraise_error=True).has(
            parameter('--param', required=True),
        )
        assert_cli_error(lambda: cli.run())
