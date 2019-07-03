from cliglue import *
from tests.asserts import MockIO
from tests.parser.actions import *


def test_setting_flag():
    with MockIO('--force', 'run') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_flag_force),
            flag('--force'),
        ).run()
        assert mockio.output() == 'force: True\n'
    with MockIO('run', '-f') as mockio:
        CliBuilder().has(
            subcommand('run', run=print_flag_force),
            flag('--force', '-f'),
        ).run()
        assert mockio.output() == 'force: True\n'


def test_only_flag():
    with MockIO('--force') as mockio:
        CliBuilder(run=print_flag_force).has(
            flag('--force', '-f'),
        ).run()
        assert mockio.output() == 'force: True\n'


def test_no_flag_set():
    with MockIO() as mockio:
        CliBuilder(run=print_flag_force).has(
            flag('--force', '-f'),
        ).run()
        assert mockio.output() == 'force: False\n'


def test_no_flag_defined():
    with MockIO('--force') as mockio:
        CliBuilder(run=print_flag_force).run()
        assert 'force: None' in mockio.output()


def test_adding_flag_by_name():
    with MockIO('--force') as mockio:
        CliBuilder(run=print_flag_force).has(
            flag('force'),
        ).run()
        assert mockio.output() == 'force: True\n'


def test_adding_flag_by_short_name():
    def print_flag_f(f: bool):
        print(f'force: {f}')

    with MockIO('-f') as mockio:
        CliBuilder(run=print_flag_f).has(
            flag('f'),
        ).run()
        assert mockio.output() == 'force: True\n'


def test_dashed_param_name():
    def print_flag(skip_it: bool):
        print(f'skip_it: {skip_it}')

    with MockIO('--skip-it') as mockio:
        CliBuilder(run=print_flag).has(
            flag('skip-it'),
        ).run()
        assert mockio.output() == 'skip_it: True\n'
