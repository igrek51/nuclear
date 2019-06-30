from cliglue import *
from tests.asserts import MockIO


def test_primary_option_cancels_required_args():
    with MockIO('--help') as mockio:
        CliBuilder(with_defaults=True).run()
        assert 'Usage' in mockio.output()
        assert 'Syntax error' not in mockio.output()
