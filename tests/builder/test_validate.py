from nuclear import *
from tests.asserts import MockIO, assert_cli_error


def test_error_pos_arg_after_unlimited_many_args():
    with MockIO():
        cli = CliBuilder(reraise_error=True).has(
            arguments('unlimited'),
            argument('next'),
        )
        assert_cli_error(lambda: cli.run())
