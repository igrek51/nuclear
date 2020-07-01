from nuclear import *
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
        CliBuilder(run=print_flag_force, error_unrecognized=False).run()
        assert 'force: None' in mockio.output()
    with MockIO('--force') as mockio:
        CliBuilder(run=print_flag_force, error_unrecognized=True).run()
        assert 'unrecognized arguments' in mockio.output()


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


def test_multi_flag():
    def print_flag(verbose: int, v: int):
        print(f'verbose: {verbose} {v}')

    with MockIO('-v', '--verbose', '-v') as mockio:
        CliBuilder(run=print_flag).has(
            flag('verbose', 'v', multiple=True),
        ).run()
        assert mockio.output() == 'verbose: 3 3\n'

    with MockIO() as mockio:
        CliBuilder(run=print_flag).has(
            flag('verbose', 'v', multiple=True),
        ).run()
        assert mockio.output() == 'verbose: 0 0\n'


def test_combined_short_single_flags():
    def print_flags(t: bool, u: bool, l: bool):
        print(f'flags: {t} {u} {l}')

    with MockIO('-tul') as mockio:
        CliBuilder(run=print_flags).has(
            flag('t'),
            flag('u'),
            flag('l'),
        ).run()
        assert mockio.stripped() == 'flags: True True True'


def test_combined_short_multi_flag():
    def print_flags(verbose: int):
        print(f'verbose level: {verbose}')

    with MockIO('-vvv') as mockio:
        CliBuilder(run=print_flags).has(
            flag('verbose', 'v', multiple=True),
        ).run()
        assert mockio.stripped() == 'verbose level: 3'

    with MockIO() as mockio:
        CliBuilder(run=print_flags).has(
            flag('verbose', 'v', multiple=True),
        ).run()
        assert mockio.stripped() == 'verbose level: 0'
