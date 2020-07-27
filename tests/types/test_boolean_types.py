from nuclear import *
from nuclear.types.boolean import boolean
from tests.asserts import MockIO


def test_boolean_type():
    def print_it(param1: bool, param2: bool):
        print(f'{param1} {type(param1).__name__}, {param2} {type(param2).__name__}')

    with MockIO('--param1=true') as mockio:
        CliBuilder(run=print_it).has(
            parameter('param1', type=boolean, default=False),
            parameter('param2', type=boolean, default=True),
        ).run()
        assert mockio.stripped() == 'True bool, True bool'

    with MockIO('--param1=false', '--param2=no') as mockio:
        CliBuilder(run=print_it).has(
            parameter('param1', type=boolean, default=True),
            parameter('param2', type=boolean, default=True),
        ).run()
        assert mockio.stripped() == 'False bool, False bool'
