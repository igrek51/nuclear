from cliglue.builder import *
from tests.testing_utils import MockIO
from .actions import *


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
