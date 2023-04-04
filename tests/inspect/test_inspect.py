from nuclear import CliBuilder, argument, inspect
from nuclear.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert output == "str: None\ntype: <class 'NoneType'>"

    output = inspect_format([5])
    assert output == """
str: [5]
type: <class 'list'>
doc: Built-in mutable sequence.

Public attributes:
  def append(object, /): Append object to the end of the list.
  def clear(): Remove all items from list.
  def copy(): Return a shallow copy of the list.
  def count(value, /): Return number of occurrences of value.
  def extend(iterable, /): Extend list by appending elements from the iterable.
  def index(value, start=0, stop=9223372036854775807, /): Return first index of value.
  def insert(index, object, /): Insert object before index.
  def pop(index=-1, /): Remove and return item at index (default last).
  def remove(value, /): Remove first occurrence of value.
  def reverse(): Reverse *IN PLACE*.
  def sort(*, key=None, reverse=False): Sort the list in ascending order and return None.
""".strip()
    
    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /): Return self==value." in output


def test_inspect_object():
    class Hero:
        def __init__(self, name: str):
            self.a = name
        
        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness
    
    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, r'''
str: <test_inspect\.test_inspect_object\.<locals>\.Hero object at .*>
type: <class 'test_inspect\.test_inspect_object\.<locals>\.Hero'>

Public attributes:
  a: <class 'str'> = batman

  def shout\(loudness: int\) -> str: Do something very very very very very very very very very very very very very very very very very st\.\.\.
''')


def test_inspect_clibuilder():
    cli = CliBuilder().has(argument('n', type=int))
    inspect(cli)
    output = inspect_format(cli)
    assert_multiline_match(output, r'''
str: <nuclear\.builder\.builder\.CliBuilder object at .*>
type: <class 'nuclear.builder.builder.CliBuilder'>

Public attributes:
  def add_command\(\*subcommands: str\): Decorator for binding function with a CLI command
  def has\(\*subrules: nuclear.builder.rule.CliRule\) -> 'CliBuilder': Add more CLI rules for the particular level
  def print_help\(subcommands: List\[str\]\)
  def print_usage\(\)
  def run\(\): Parse all the CLI arguments passed to application.
  def run_with_args\(args: List\[str\]\)

Private attributes:
  _CliBuilder__error_unrecognized: <class 'bool'> = True
  _CliBuilder__help: <class 'NoneType'> = None
  _CliBuilder__help_on_empty: <class 'bool'> = False
  _CliBuilder__hide_internal: <class 'bool'> = True
  _CliBuilder__log_error: <class 'bool'> = False
  _CliBuilder__name: <class 'NoneType'> = None
  _CliBuilder__reraise_error: <class 'bool'> = False
  _CliBuilder__subrules: <class 'list'> = \[PrimaryOptionRule\(help='Display this help and exit', keywords={.*}, run=<function CliBu\.\.\.
  _CliBuilder__usage_onerror: <class 'bool'> = True
  _CliBuilder__version: <class 'NoneType'> = None

  def _CliBuilder__add_default_rules\(\)
  def _CliBuilder__bash_autocomplete\(cmdline: str, word_idx: Optional\[int\]\)
  def _CliBuilder__bind_decorated_command\(function: Callable\[\.\.\., NoneType\], names: List\[str\]\)
  def _CliBuilder__create_parser\(args: List\[str\]\) -> nuclear.parser.parser.Parser
  def _CliBuilder__find_subcommand_rule\(name: str\) -> Optional\[nuclear.builder.rule.SubcommandRule\]
  def _CliBuilder__has_default_action\(\) -> bool
''')