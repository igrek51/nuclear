from cliglue import *
from tests.asserts import MockIO


def test_empty_builder():
    with MockIO() as mockio:
        CliBuilder()
        assert mockio.output() == ''
    with MockIO():
        CliBuilder(with_defaults=False).run()
