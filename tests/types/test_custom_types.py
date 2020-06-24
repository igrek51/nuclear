from nuclear import *
from tests.asserts import MockIO


def test_custom_parser():
    def my_parser(arg):
        return eval(arg)

    def print_my(my):
        print(my)

    with MockIO('--my=17+5') as mockio:
        CliBuilder(run=print_my).has(
            parameter('my', type=my_parser),
        ).run()
        assert mockio.stripped() == '22'


def test_type_none():
    with MockIO('--param', 'notanumber') as mockio:
        CliBuilder(reraise_error=True, run=lambda param: print(param)).has(
            parameter('param', type=None),
        ).run()
        assert 'notanumber' in mockio.stripped()
