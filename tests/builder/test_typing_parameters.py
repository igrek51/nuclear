from typing import Optional, Union, Dict
from datetime import datetime

import pytest
from nuclear import CliBuilder
from nuclear.cli.parser.error import CliSyntaxError
from tests.asserts import MockIO


def test_optional_type_param():
    cli = CliBuilder()
    @cli.add_command("run")
    def run(backend: Optional[str] = None):
        print(f"backend: {backend}")

    with MockIO('run', '--backend', 'jack') as mockio:
        cli.run()
        assert mockio.output() == "backend: jack\n"
    with MockIO('run') as mockio:
        cli.run()
        assert mockio.output() == "backend: None\n"


def test_union_type_param():
    cli = CliBuilder(reraise_error=True)
    @cli.add_command("run")
    def run(temperature: Optional[Union[Union[datetime, Dict], Union[int, float]]] = None):
        print(f"temperature: {temperature}")

    with MockIO('run', '--temperature', '1.0') as mockio:
        cli.run()
        assert mockio.output() == "temperature: 1.0\n"
    with MockIO('run', '--temperature', '5') as mockio:
        cli.run()
        assert mockio.output() == "temperature: 5\n"
    with MockIO('run') as mockio:
        cli.run()
        assert mockio.output() == "temperature: None\n"
    with MockIO('run', '--temperature', 'hot') as mockio:
        with pytest.raises(CliSyntaxError) as excinfo:
            cli.run()
        assert "variable 'hot' didn't match Union type" in str(excinfo.value)


def test_dict_type_param():
    cli = CliBuilder(reraise_error=True)
    @cli.add_command("run")
    def run(names: Dict[str, str]):
        print(f"names: {names}")

    with MockIO('run', '{}') as mockio:
        cli.run()
        assert mockio.output() == "names: {}\n"
