from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from nuclear import CliBuilder, argument, inspect, wat
from nuclear.inspection.inspection import inspect_format
from tests.asserts import assert_multiline_match, remove_ansi_sequences, StdoutCap


def test_inspect_primitive_var():
    output = inspect_format(None)
    assert remove_ansi_sequences(output) == """
value: None
type: NoneType
""".strip()

    output = inspect_format([5])
    assert remove_ansi_sequences(output) == """
value: [
    5,
]
type: list
len: 1

Public attributes:
  def append(object, /) # Append object to the end of the list.
  def clear() # Remove all items from list.
  def copy() # Return a shallow copy of the list.
  def count(value, /) # Return number of occurrences of value.
  def extend(iterable, /) # Extend list by appending elements from the iterable.
  def index(value, start=0, stop=9223372036854775807, /) # Return first index of value.…
  def insert(index, object, /) # Insert object before index.
  def pop(index=-1, /) # Remove and return item at index (default last).…
  def remove(value, /) # Remove first occurrence of value.…
  def reverse() # Reverse *IN PLACE*.
  def sort(*, key=None, reverse=False) # Sort the list in ascending order and return None.…
""".strip()
    
    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in remove_ansi_sequences(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r'''
value: 'poo'
type: str
len: 3
''')


def test_inspect_instance():
    class Hero:
        """
        A hero
        """
        def __init__(self, name: str):
            self.a = name
        
        def shout(self, loudness: int) -> str:
            """Do something very very very very very very very very very very very very very very very very very stupid"""
            return self.a * loudness
    
    instance = Hero('batman')
    output = inspect_format(instance)
    assert_multiline_match(output, r'''
value: <test_inspect\.test_inspect_instance\.<locals>\.Hero object at .*>
type: test_inspect\.Hero

Public attributes:
  a: str = 'batman'

  def shout\(loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…
''')
                           
    output = inspect_format(Hero)
    assert_multiline_match(output, r'''
value: <class 'test_inspect\.test_inspect_instance\.<locals>\.Hero'>
type: type
signature: class Hero\(name: str\)
"""A hero"""

Public attributes:
  def shout\(self, loudness: int\) -> str \# Do something very very very very very very very very very very very very very very very very very st…
''')


def test_inspect_clibuilder():
    cli = CliBuilder().has(argument('n', type=int))
    inspect(cli)
    output = inspect_format(cli)
    assert_multiline_match(output, r'''
value: <nuclear\.builder\.builder\.CliBuilder object at .*>
type: nuclear.builder.builder.CliBuilder

Public attributes:
  def add_command\(\*subcommands: str\) \# Decorator for binding function with a CLI command…
  def has\(\*subrules: nuclear.builder.rule.CliRule\) -> 'CliBuilder' \# Add more CLI rules for the particular level…
  def print_help\(subcommands: List\[str\]\)
  def print_usage\(\)
  def run\(\) \# Parse all the CLI arguments passed to application.…
  def run_with_args\(args: List\[str\]\)

Private attributes:
  _CliBuilder__error_unrecognized: bool = True
  _CliBuilder__help: NoneType = None
  _CliBuilder__help_on_empty: bool = False
  _CliBuilder__hide_internal: bool = True
  _CliBuilder__log_error: bool = False
  _CliBuilder__name: NoneType = None
  _CliBuilder__reraise_error: bool = False
  _CliBuilder__subrules: list = \[…
  _CliBuilder__usage_onerror: bool = True
  _CliBuilder__version: NoneType = None

  def _CliBuilder__add_default_rules\(\)
  def _CliBuilder__bash_autocomplete\(cmdline: str, word_idx: Optional\[int\]\)
  def _CliBuilder__bind_decorated_command\(function: Callable\[\.\.\., NoneType\], names: List\[str\]\)
  def _CliBuilder__create_parser\(args: List\[str\]\) -> nuclear.parser.parser.Parser
  def _CliBuilder__find_subcommand_rule\(name: str\) -> Optional\[nuclear.builder.rule.SubcommandRule\]
  def _CliBuilder__has_default_action\(\) -> bool
''')


def test_inspect_function():
    def foo(a: int, b: str = 'bar') -> str:
        """
        Do something
        dumb
        """
        return a * b
  
    output = inspect_format(foo)
    print(output)
    assert_multiline_match(output, r'''
value: <function test_inspect_function\.<locals>\.foo at .*>
type: function
signature: def foo\(a: int, b: str = 'bar'\) -> str
"""
Do something
dumb
"""
''')


def test_inspect_nested_dict():
    output = inspect_format({
        'a': {
            'b': {
                'values': [2,5,3],
            },
            "empty_dict": {},
            "empty_list": [],
            40: None,
            None: 42,
        },
    }, short=True)
    assert_multiline_match(output, r'''
value: {
    'a': {
        'b': {
            'values': \[
                2,
                5,
                3,
            \],
        },
        'empty_dict': {},
        'empty_list': \[\],
        40: None,
        None: 42,
    },
}
type: dict
len: 1
''')


def test_inspect_datetime_repr():
    output = inspect_format(datetime(2023, 8, 1), short=True)
    assert_multiline_match(output, r'''
str: 2023-08-01 00:00:00
repr: datetime.datetime\(2023, 8, 1, 0, 0\)
type: datetime.datetime
parents: datetime\.date
''')


def test_inspect_source_code():
    output = inspect_format(datetime, long=True, code=True)
    lines = output.splitlines()
    assert "value: <class 'datetime.datetime'>" in lines
    assert "type: type" in lines
    assert "signature: class datetime(…)" in lines
    assert "datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])" in lines
    assert "class datetime(date):" in lines


def test_inspect_async_def():
    async def looper():
        pass
    output = inspect_format(looper, short=True)
    assert_multiline_match(output, r'''
value: <function test_inspect_async_def.<locals>.looper at .*>
type: function
signature: async def looper\(\)
''')


def test_wat_with_nothing():
    assert str(wat) == '<nuclear Wat Inspector object>'
    with StdoutCap() as capture:
        assert repr(wat) == ''
    assert 'Try `wat / object`, `wat(**options) / object` or `wat(object, **options)` to inspect an object. Options are:' in capture.uncolor().splitlines()


def test_wat_with_object():
    with StdoutCap() as capture:
        wat(short=True) / 'moo'
    assert_multiline_match(capture.output(), r'''
value: 'moo'
type: str
len: 3
''')

    with StdoutCap() as capture:
        wat('moo', short=True)
    assert_multiline_match(capture.output(), r'''
value: 'moo'
type: str
len: 3
''')


def test_list_parent_classes():
    class Parent(str, Enum):
        FIRST = 'first'

    output = inspect_format(Parent.FIRST, short=True)
    assert_multiline_match(output, r'''
str: 'Parent.FIRST'
repr: <Parent\.FIRST: 'first'>
type: test_inspect\.Parent
parents: str, enum\.Enum
len: 5
''')


def test_pydantic_class():
    class Person(BaseModel):
        name: str

    output = inspect_format(Person(name='george'), short=True)
    assert_multiline_match(output, r'''
str: name='george'
repr: Person\(name='george'\)
type: test_inspect\.Person
parents: pydantic\.main\.BaseModel
''')
