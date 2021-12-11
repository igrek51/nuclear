from nuclear import *
from nuclear.parser.error import CliDefinitionError
from tests.asserts import MockIO, assert_error
from functools import reduce
import base64


cli = CliBuilder()


@cli.add_command('hello')
def say_hello(name: str, decode: bool = False, repeat: int = 1):
    """
    Say hello to someone
    :param name: Name to say hello to
    :param decode: Decode name as base64
    """
    if decode:
        name = base64.b64decode(name).decode('utf-8')
    print(' '.join([f"I'm a {name}!"] * repeat))


@cli.add_command('calculate', 'factorial')
def calculate_factorial(n: int):
    """Calculate factorial"""
    result = reduce(lambda x, y: x * y, range(1, n + 1))
    print(result)
    return result


@cli.add_command('calculate', 'primes')
def calculate_primes(n: int = 100):
    """
    List prime numbers using Sieve of Eratosthenes
    
    :param n: maximum number to check
    """
    print(sorted(reduce((lambda r, x: r - set(range(x**2, n, x)) if (x in r) else r), 
                        range(2, n), set(range(2, n)))))


def test_calling_subcommand():
    with MockIO('hello', 'world') as mockio:
        cli.run()
        assert mockio.output() == "I'm a world!\n"
    with MockIO('calculate', 'factorial', '6') as mockio:
        cli.run()
        assert mockio.output() == "720\n"
    with MockIO('calculate', 'primes', '-n=10') as mockio:
        cli.run()
        assert mockio.output() == "[2, 3, 5, 7]\n"


def test_bool_flag():
    @cli.add_command('print very stupid flag')
    def print_something_very_stupid(force: bool):
        print(f"argument: {force}")

    @cli.add_command('test flaggy default_false')
    def flaggy_false(force: bool = False):
        print(f"flag: {force}")

    @cli.add_command('test flaggy default_true')
    def flaggy_true(force: bool = True):
        print(f"parameter: {force}")

    with MockIO('print', 'very', 'stupid', 'flag', 'false') as mockio:
        cli.run()
        assert mockio.output() == "argument: False\n"

    with MockIO('test', 'flaggy', 'default_false') as mockio:
        cli.run()
        assert mockio.output() == "flag: False\n"
    with MockIO('test', 'flaggy', 'default_false', '--force') as mockio:
        cli.run()
        assert mockio.output() == "flag: True\n"

    with MockIO('test', 'flaggy', 'default_true') as mockio:
        cli.run()
        assert mockio.output() == "parameter: True\n"
    with MockIO('test', 'flaggy', 'default_true', '--force=false') as mockio:
        cli.run()
        assert mockio.output() == "parameter: False\n"


def test_function_calling_works_after_decorating():
    assert calculate_factorial(6) == 720


def test_no_subcommand_name_error():
    def do_something_evil():
        @cli.add_command()
        def do_nothing(n: int):
            print('nothing')
    assert_error(do_something_evil, error_type=CliDefinitionError)


def test_varargs_with_kwonly_args():
    @cli.add_command('doit')
    def doit(*numbers: int, temperature = 0, force: bool = False):
        print(f"args: {numbers}, temperature: {temperature}, force: {force}")

    with MockIO('doit', '1', '2', '--temperature', '36', '--force') as mockio:
        cli.run()
        assert mockio.output() == "args: (1, 2), temperature: 36, force: True\n"


def test_extract_param_docstring_to_help():
    with MockIO('--help') as mockio:
        cli.run()
        assert 'Say hello to someone' in mockio.output()
        assert ':param' not in mockio.output()

    with MockIO('hello', '--help') as mockio:
        cli.run()
        assert 'Decode name as base64' in mockio.output()
        assert 'NAME - Name to say hello to' in mockio.output()
        assert ':param' not in mockio.output()
