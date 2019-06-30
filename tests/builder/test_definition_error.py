from cliglue import *
from cliglue.parser.error import CliDefinitionError
from tests.asserts import assert_error


def test_multilevel_commands_usage():
    cli = CliBuilder().has(
        parameter('d', required=True, default='42'),
    )
    assert_error(lambda: cli.run(), error_type=CliDefinitionError)
