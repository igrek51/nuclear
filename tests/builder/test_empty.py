from cliglue.builder import *
from tests.testing_utils import MockIO


def test_empty_builder():
    with MockIO() as mockio:
        CliBuilder()
        mockio.assert_output('')
    with MockIO():
        CliBuilder().run()
