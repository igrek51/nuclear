# -*- coding: utf-8 -*-
import mock

from glue import *

# import StringIO (Python 2 and 3 compatible)
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


# ------- Testing tools -------

def assert_error(action, expected_error=None):
    try:
        action()
        assert False
    except RuntimeError as e:
        if expected_error:
            assert expected_error in str(e)


def assert_system_exit(action):
    try:
        action()
        assert False
    except SystemExit as e:
        # exit with error code 0
        assert str(e) == '0'


def assert_ap_error(ap, expected_error=None):
    assert_error(lambda: ap.process(), expected_error)


class MockIO:
    def __init__(self, in_args_list=None):
        # mock cli input
        if not in_args_list:
            in_args_list = []
        self.in_args_list = in_args_list
        self._mock_args = mock.patch.object(sys, 'argv', ['glue'] + self.in_args_list)
        # mock output
        self.new_out, self.new_err = StringIO(), StringIO()
        self.old_out, self.old_err = sys.stdout, sys.stderr

    def __enter__(self):
        self._mock_args.__enter__()
        sys.stdout, sys.stderr = self.new_out, self.new_err
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._mock_args.__exit__(exc_type, exc_value, traceback)
        sys.stdout, sys.stderr = self.old_out, self.old_err

    def output(self):
        return self.new_out.getvalue()

    def output_strip(self):
        return self.output().strip()

    def output_contains(self, in_str):
        return in_str in self.output()

    def assert_output_contains(self, in_str):
        assert in_str in self.output()
        return True

    def assert_output(self, in_str):
        assert in_str == self.output()
        return True


# ------- TESTS -------

def test_output():
    with MockIO() as mockio:
        debug('message')
        assert mockio.output_contains('message')
        assert mockio.output_contains('debug')
        info('message')
        assert mockio.output_contains('info')
        warn('message')
        assert mockio.output_contains('warn')
        error('message')
        assert mockio.output_contains('ERROR')
        info(7)
        assert mockio.output_contains('7')


def test_fatal():
    assert_error(lambda: fatal('fatality'))
    assert_error(lambda: fatal('fatality'), 'fatality')
    assert_system_exit(lambda: exit_now('farewell'))
    assert_system_exit(lambda: exit_now())


def test_shell_exec():
    shell('echo test')
    assert_error(lambda: shell('dupafatality'))
    assert shell_error_code('echo test') == 0
    assert shell_output('echo test') == 'test\n'
    assert shell_output('echo żółć') == u'żółć\n'
    assert shell_output('echo test', as_bytes=True) == b'test\n'
    assert shell_output('echo test', as_bytes=True) == 'test\n'.encode('utf-8')
    assert shell_output('echo test', as_bytes=True).decode('utf-8') == 'test\n'


def test_split_lines():
    assert split_lines('a\nb\nc') == ['a', 'b', 'c']
    assert split_lines('\na\n\n') == ['a']
    assert split_lines('\n\n\n') == []
    assert split_lines('') == []
    assert split_lines('a\n\n\r\nb') == ['a', 'b']


def test_split_to_tuple():
    assert split_to_tuple('a', 1) == ('a',)
    assert split_to_tuple('', 1) == ('',)
    assert_error(lambda: split_to_tuple('a', 2))
    assert split_to_tuple('a\tb', 2) == ('a', 'b')
    assert_error(lambda: split_to_tuple('a\tb', 1))
    assert_error(lambda: split_to_tuple('a\tb\t', 2))
    assert split_to_tuple('a\tb\t', 3) == ('a', 'b', '')
    assert split_to_tuple('a\tb\tc', 3) == ('a', 'b', 'c')
    assert split_to_tuple('a b c', 3, ' ') == ('a', 'b', 'c')
    # no attrsCount verification
    assert split_to_tuple('a b c', splitter=' ') == ('a', 'b', 'c')
    assert split_to_tuple('a') == ('a',)


def test_split_to_tuples():
    assert split_to_tuples('a\tb\tc\nd\te\tf', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('\n\na\tb\tc\n\nd\te\tf\n', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('a\tb\tc', 3) == [('a', 'b', 'c')]
    # splitted list as input
    assert split_to_tuples(['a\tb\tc', 'd\te\tf'], 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples(['a\tb\tc'], 3) == [('a', 'b', 'c')]


def test_regex_replace():
    assert regex_replace('abca', 'a', 'b') == 'bbcb'
    assert regex_replace('abc123a', r'\d', '5') == 'abc555a'


def test_regex_match():
    assert regex_match('ab 12 def 123', r'.*\d{2}')
    assert not regex_match('ab 1 def 1m2', r'.*\d{2}.*')


def test_regex_list():
    # regexReplaceList
    assert regex_replace_list(['a', 'b', '25', 'c'], r'\d+', '7') == ['a', 'b', '7', 'c']
    assert regex_replace_list(['a1', '2b', '3', ''], r'\d', '7') == ['a7', '7b', '7', '']
    assert regex_replace_list(['a1', '2b', '3', ''], r'.*\d.*', '7') == ['7', '7', '7', '']
    # regexFilterLines
    assert regex_filter_list(['a1', '2b', '3', ''], r'.*\d.*') == ['a1', '2b', '3']
    assert regex_filter_list(['a1', '2b', '3', ''], r'dupa') == []
    # regexSearchFile
    assert regex_search_file('test/res/findme', r'\t*<author>(\w*)</author>', 1) == 'Anonim'
    assert regex_search_file('test/res/findme', r'\t*<name>(\w*)</name><sur>(\w*)</sur>', 2) == 'Sur'
    # regexReplaceFile
    save_file('test/res/replaceme', 'dupa\n123')
    assert regex_replace_file('test/res/replaceme', r'[a-z]+', 'letters') == 'letters\n123'


def test_input_string():
    sys.stdin = open('test/res/inputs')
    assert input_string() == 'in1'
    assert input_string('prompt') == 'in2'


def test_input_required():
    sys.stdin = open('test/res/inputRequired')
    assert input_required('required: ') == 'valid'


def test_read_file():
    assert read_file('test/res/readme') == 'Readme\n123'


def test_save_file():
    save_file('test/res/saveme', 'dupa\n123')
    assert read_file('test/res/saveme') == 'dupa\n123'
    save_file('test/res/saveme', '')
    assert read_file('test/res/saveme') == ''


def test_list_dir():
    assert list_dir('test/res/listme') == ['afile', 'dir', 'zlast', 'zlastdir']


def test_workdir():
    workdir = get_workdir()
    set_workdir('/')
    assert get_workdir() == '/'
    set_workdir('/home/')
    assert get_workdir() == '/home'
    set_workdir(workdir)


def test_script_real_dir():
    real_dir_expected = get_workdir()
    assert script_real_dir() == real_dir_expected


def test_script_real_path():
    assert '/pytest.py' in script_real_path()


def test_file_exists():
    assert file_exists('test/res/readme')
    assert not file_exists('test/res/dupadupa')


def test_filter_list():
    assert filter_list(lambda e: len(e) <= 3, ['a', '123', '12345']) == ['a', '123']


def test_map_list():
    assert map_list(lambda e: e + e, ['a', '123', '']) == ['aa', '123123', '']


def test_time_conversions():
    pattern = '%H:%M:%S, %d.%m.%Y'
    sample_date = '16:26:01, 20.12.2017'
    bad_date = '16:26:01 20.12.17dupa'
    datetime = str2time(sample_date, pattern)
    assert datetime is not None
    assert time2str(datetime, pattern) == sample_date
    assert str2time(bad_date, pattern) is None
    assert time2str(None, pattern) is None


# CLI parser
def test_cli_arg_rule():
    assert CliArgRule(keywords='name', description='description',
                      syntax='syntaxSuffix')._display_syntax_prefix() == 'name'
    assert CliArgRule(keywords=['name1', 'name2'], description='description',
                      syntax='syntaxSuffix')._display_syntax_prefix() == 'name1, name2'
    assert CliArgRule(keywords=['name1', 'name2'], description='description',
                      syntax=None).display_syntax() == 'name1, name2'
    assert CliArgRule(keywords=['name1', 'name2'], description='description',
                      syntax='<suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CliArgRule(keywords=['name1', 'name2'], description='description',
                      syntax=' <suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CliArgRule(keywords=['name'], description='description', syntax=None).display_help(
        5) == 'name  - description'
    assert CliArgRule(keywords=['name'], description='description', syntax=None).display_help(3) == 'name - description'
    assert CliArgRule(keywords=['name'], description='description', syntax='<suffix>').display_help(
        3) == 'name <suffix> - description'
    assert CliArgRule(keywords=['name'], description='description', syntax='<s>').display_help(
        10) == 'name <s>   - description'


# ArgsProcessor
def command1():
    print('None')


def action_dupa():
    print('dupa')


def command2(ap):
    param = ap.poll_next('param')
    print(param)
    return param


def command3(ap):
    param = ap.peek_next()
    if not param:
        assert not ap.has_next()
    param2 = ap.poll_next()
    assert param == param2
    print(param)


def command4Remaining(ap):
    print(ap.poll_remaining_joined())


def commandpollRemaining(ap):
    print(ap.poll_remaining())


def command5Poll(ap):
    while (ap.has_next()):
        print(ap.poll_next())


def command6SetPara(ap):
    para = ap.poll_next('para')
    ap.set_param('para', para)


def commandPrintVersionOnly(ap):
    ap.print_version()


def actionIsForce(ap):
    print('force is: ' + str(ap.is_flag_set('force')))


def actionIsF(ap):
    print('force is: ' + str(ap.is_flag_set('f')))


def sample_processor1():
    ap = ArgsProcessor('appName', '1.0.1')
    ap.add_subcommand('command1', action=command1, description='description1')
    ap.add_subcommand(['command2', 'command22'], action=command2, description='description2', syntax='<param>')
    ap.add_subcommand(['command3', 'command33'], action=command3, description='description2', syntax='<param>')
    ap.add_subcommand('remain', action=command4Remaining, description='description4', syntax='<param>')
    ap.add_subcommand('poll', action=command5Poll, description='description5')
    ap.add_subcommand('--set-para', action=command6SetPara, description='set para')
    return ap


def test_args_simple_command():
    with MockIO(['du']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('du', action_dupa)
        ap.process()
        mockio.output_contains('dupa')


def test_args_test_help():
    # basic execution with no args
    with MockIO(['help']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('help', print_help)
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def test_argsprocessor_noarg():
    # basic execution with no args
    with MockIO([]) as mockio:
        ArgsProcessor('appName', '1.0.1').process()
        assert mockio.output_contains('Usage:')  # prints help


def test_argsprocessor_bindings_setup():
    # test bindings setup
    with MockIO([]) as mockio:
        sample_processor1()


def test_argsprocessor_bind_default_action():
    # test bindings
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_dupa)
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['-h']) as mockio:
        ap = ArgsProcessor(default_action=command1)
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def action_print_param1(ap):
    print(ap.get_param('param'))


def test_args_params_first():
    # test processing params first
    with MockIO(['print-param', '--param=dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('dupa')
    with MockIO(['print-param', '--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('dupa')
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-param', action_print_param1)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def action_print_flag(ap):
    print(ap.is_flag_set('dupcia'))


def test_args_print_flag():
    # test processing params first
    with MockIO(['print-flag', '--dupcia']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-flag', action_print_flag)
        ap.add_flag('dupcia')
        ap.process()
        assert mockio.output_contains('True')
    with MockIO(['print-flag', '--dup']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('print-flag', action_print_flag)
        ap.add_flag('dupcia')
        ap.process()
        assert mockio.output_contains('False')


def test_args_no_next_arg():
    # test lack of next argument
    with MockIO(['command2']) as mockio:
        sample_processor1().process()
        assert 'ERROR' in mockio.output()
        assert 'no required argument "param" given' in mockio.output()
    with MockIO(['command33']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'None\n'


def test_argsprocessor_given_param():
    # test given param
    with MockIO(['command3', 'dupa']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'dupa\n'
    with MockIO(['command2', 'dupa']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'dupa\n'


def test_argsprocessor_binding():
    # test binding with no argProcessor
    with MockIO(['command1']) as mockio:
        sample_processor1().process()
        assert mockio.output() == 'None\n'


def test_argsprocessor_poll_remaining_joined():
    # test pollRemainingJoined():
    with MockIO(['remain']) as mockio:
        sample_processor1().process()
        assert mockio.output() == '\n'
    with MockIO(['remain', '1']) as mockio:
        sample_processor1().process()
        assert mockio.output_strip() == '1'
    with MockIO(['remain', '1', 'abc', 'd']) as mockio:
        sample_processor1().process()
        assert mockio.output_strip() == '1 abc d'


def test_argsprocessor_poll_remaining():
    with MockIO(['remaining', 'jasna', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=commandpollRemaining)
        ap.process()
        assert mockio.output_strip() == "['remaining', 'jasna', 'dupa']"


def test_args_poll():
    # test polling
    with MockIO(['poll', '123', '456', '789']) as mockio:
        sample_processor1().process()
        assert mockio.output() == '123\n456\n789\n'


def action_test_args_params_with_hyphens(ap):
    print(ap.get_param('--param-one'))
    print(ap.get_param('param-one'))
    print(ap.get_param('param2'))
    print(ap.get_param('--param2'))
    print(ap.get_param('p'))


def test_args_params_with_hyphens():
    with MockIO(['--param-one', 'value-one', '--param2', 'p2', '-p', 'p3']) as mockio:
        ap = ArgsProcessor(default_action=action_test_args_params_with_hyphens)
        ap.add_param('--param-one')
        ap.add_param('param2')
        ap.add_param('p')
        ap.process()
        assert mockio.output() == 'value-one\nvalue-one\np2\np2\np3\n'


def action_print_remaining(ap):
    print(ap.poll_remaining_joined())


def test_args_removing_args():
    # test removing parameters
    with MockIO(['remain', 'jasna', '--to-remove', 'dupa', 'dupaa', '--flagg', 'abc', '1']) as mockio:
        ap = ArgsProcessor()
        ap.add_param('--to-remove')
        ap.add_flag('--flagg')
        ap.add_subcommand('remain', action_print_remaining)
        ap.process()
        assert mockio.output() == 'jasna dupaa abc 1\n'


def action_nothing():
    pass


def test_args_unknown_arg():
    # test unknown argument
    with MockIO(['jasna', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_nothing)
        ap.process()
        assert 'invalid arguments: jasna dupa' in mockio.output()


def test_args_default_action():
    with MockIO(['dupa']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command2)
        ap.process()
        assert mockio.output() == 'dupa\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command2)
        ap.process()
        assert mockio.output() == 'None\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=print_help)
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
    # test getting params
    with MockIO(['dupa2']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command2)
        ap.process()
        assert mockio.output() == 'dupa2\n'


def test_args_bind_default_options():
    with MockIO(['-v']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output() == 'appName v1.0.1\n'
    with MockIO(['-v', '-v']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output_contains('appName v1.0.1\n')
        assert mockio.output_contains('invalid arguments')
    with MockIO(['-h']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help


def action_set_object_param(ap):
    ap.set_param('numberek', int(7))


def test_args_object_params():
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_set_object_param)
        ap.process()
        assert not ap.is_param('dupa')
        assert ap.get_param('dupa') is None
        assert ap.is_param('numberek')
        assert ap.get_param('numberek') is 7


def test_args_options_and_default_acction():
    with MockIO(['-v2', '-v2']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=command1)
        ap.add_subcommand(command1, 'command1', description='description1')
        ap.process()
        assert mockio.output_contains('None')
        assert mockio.output_contains('invalid arguments')
        assert mockio.output_contains('v2')


def test_args_toomanyargs():
    with MockIO(['command1', 'two', 'much']) as mockio:
        sample_processor1().process()
        assert 'None' in mockio.output()
        assert 'invalid arguments: two much' in mockio.output()


def test_argsprocessor_bind_flag():
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('force').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['--force']) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('force').process()
        assert mockio.output() == 'force is: True\n'
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('force', '--for').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['--for']) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('force', '--for').process()
        assert mockio.output() == 'force is: True\n'
    # single letter
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('f').process()
        assert mockio.output() == 'force is: False\n'
    with MockIO(['-f']) as mockio:
        ap = ArgsProcessor(default_action=actionIsF)
        ap.add_flag('f').process()
        assert mockio.output() == 'force is: True\n'
    with MockIO(['-f']) as mockio:
        ap = ArgsProcessor(default_action=actionIsForce)
        ap.add_flag('force', ['-f', '--force']).process()
        assert mockio.output() == 'force is: True\n'


def action_print_params(ap):
    print('param is: %s' % ap.get_param('param'))
    print('p is: %s' % ap.get_param('p'))


def test_args_add_param():
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', description='set param').process()
        assert 'param is: None\n' in mockio.output()
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', description='set param').process()
        assert 'param is: dupa\n' in mockio.output()
    with MockIO(['--parameter', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('param', keywords='--parameter', description='set param').process()
        assert 'param is: dupa\n' in mockio.output()
    # single letter
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('p', description='set param').process()
        assert 'p is: None\n' in mockio.output()
    with MockIO(['-p', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_params)
        ap.add_param('p', description='set param').process()
        assert 'p is: dupa\n' in mockio.output()


def action_print_from_to(ap):
    print('range: ' + ap.get_param('fromDate') + ' - ' + ap.get_param('toDate'))


def test_argsprocessor_2params():
    with MockIO(['print', '--from', 'today', '--to', 'tomorrow']) as mockio:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.add_param('fromDate', keywords='--from')
        ap.add_param('toDate', keywords='--to')
        ap.add_subcommand('print', action_print_from_to)
        ap.process()
        assert 'range: today - tomorrow' in mockio.output()


def action_get_param(ap):
    print(ap.get_param('musthave', required=True))


def test_args_get_missing_required_param():
    with MockIO([]) as mockio:
        ap = ArgsProcessor('appName', '1.0.1', default_action=action_get_param)
        ap.add_param('musthave')
        ap.process()
        assert 'no required param given: musthave' in mockio.output()


def action_print_1():
    print('1')


def action_print_2():
    print('2')


def test_args_default_action():
    with MockIO([]) as mockio:
        ArgsProcessor(default_action=action_print_1).process()
        assert mockio.output_contains('1')
    # default action - help
    with MockIO([]) as mockio:
        ap = ArgsProcessor()
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
    # default action - help
    with MockIO(['print2']) as mockio:
        ap = ArgsProcessor(default_action=action_print_1)
        ap.add_subcommand('print2', action=action_print_2)
        ap.process()
        assert mockio.output_contains('2')
        assert not mockio.output_contains('1')


def test_args_add_empty_command():
    with MockIO(['test']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test')
        ap.process()
        assert mockio.output() == ''


def test_args_multilevel_commands():
    with MockIO(['test']) as mockio:
        ap = ArgsProcessor()
        ap_test = ap.add_subcommand('test')
        ap_test_dupy = ap_test.add_subcommand('dupy', action=action_print_1)
        ap_test_dupy.add_subcommand('2', action=action_print_2)
        assert mockio.output() == ''
    with MockIO(['test', 'dupy']) as mockio:
        ap = ArgsProcessor()
        ap_test = ap.add_subcommand('test')
        ap_test_dupy = ap_test.add_subcommand('dupy', action=action_print_1)
        ap_test_dupy.add_subcommand('2', action=action_print_2)
        ap.process()
        assert mockio.output().strip() == '1'
    with MockIO(['test', 'dupy', '2']) as mockio:
        ap = ArgsProcessor()
        ap_test = ap.add_subcommand('test')
        ap_test_dupy = ap_test.add_subcommand('dupy', action=action_print_1)
        ap_test_dupy.add_subcommand('2', action=action_print_2)
        ap.process()
        assert mockio.output().strip() == '2'


def action_print_param(ap):
    print(ap.get_param('param'))


def test_args_multilevel_params():
    with MockIO(['test', 'dupy', '--param=dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test').add_subcommand('dupy', action=action_print_param).add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['test', 'dupy', '--param', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('test').add_subcommand('dupy', action=action_print_param).add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'


def test_args_default_aciton_with_flags():
    with MockIO(['--flag']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_flag('flag')
        ap.process()
        assert mockio.output().strip() == 'None'


def test_args_default_aciton_with_params():
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'


def test_args_empty_param():
    with MockIO(['--param']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('no required argument "--param" given')


def test_args_required_param():
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['--none']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param')
        ap.process()
        assert mockio.output_contains('None')
        assert mockio.output_contains('invalid arguments')
    with MockIO(['--param', 'dupa']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param', required=True)
        ap.process()
        assert mockio.output().strip() == 'dupa'
    with MockIO(['--none']) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.add_param('param', required=True)
        ap.process()
        assert mockio.output_contains('missing params are required: --param')


def test_args_python3_command():
    # basic execution with no args
    with MockIO([]) as mockio:
        ap = ArgsProcessor(default_action=action_print_param)
        ap.process()
        assert mockio.output() == 'None\n'


def test_args_multilevel_commands_help():
    with MockIO(['--help']) as mockio:
        ap = ArgsProcessor('cmdline', '1.2.3')
        ap.add_param('global-param')
        ap.add_param('--global-param2', description='another parameter')
        ap.add_flag('--flag', description='a flag')
        ap_test = ap.add_subcommand('test')
        ap_test.add_param('test-param')
        ap_test_dupy = ap_test.add_subcommand('dupy', action=action_print_1)
        ap_test_dupy.add_param('z-parametrem', description='with param')
        ap_test.add_subcommand('audio', action=action_print_1, description='tests audio')
        ap_test_dupy.add_subcommand('2', action=action_print_2)
        ap.process()
        assert mockio.output_contains('Usage:')  # help
        assert mockio.output_contains('cmdline')
        assert mockio.output_contains('v1.2.3')
        assert mockio.output_contains('glue [options] <command>')
        assert mockio.output_contains('test --test-param <test-param>')
        assert mockio.output_contains('test dupy --z-parametrem <z-parametrem>')
        assert mockio.output_contains('test dupy 2')
        assert mockio.output_contains('test audio')
        assert mockio.output_contains('--global-param <global-param>')


def test_args_deafult_action_help():
    with MockIO(['--help']) as mockio:
        ap = ArgsProcessor('cmdline', '1.2.3', default_action=action_print_1, syntax=' <dupa> [optional]')
        ap.add_param('global-param')
        ap.process()
        assert mockio.output_contains('Usage:')  # prints help
        assert mockio.assert_output_contains('glue [options] <dupa> [optional]')


def action_test_args_poll_from_subcommand(ap):
    print(ap.poll_remaining_joined())


def test_args_poll_from_subcommand():
    with MockIO(['--autocomplete-install2', 'jasna', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('--autocomplete-install2', action=action_test_args_poll_from_subcommand)
        ap.process()
        assert mockio.output_strip() == 'jasna dupa'


def test_args_bash_install_permissions():
    with MockIO(['--bash-install', 'dupa']) as mockio:
        ap = ArgsProcessor()
        assert_ap_error(ap, 'failed executing')


def test_args_autocomplete():
    with MockIO(['--bash-autocomplete', 'dupa']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        assert mockio.output() == '\n'
    # test autocomplete first list commands
    with MockIO(['--bash-autocomplete', 'dupa ']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        mockio.assert_output_contains('-h\n')
        mockio.assert_output_contains('--help\n')
        mockio.assert_output_contains('-v\n')
        mockio.assert_output_contains('--version\n')
        mockio.assert_output_contains('--bash-install\n')
        mockio.assert_output_contains('--bash-autocomplete\n')
    with MockIO(['--bash-autocomplete', '"dupa "']) as mockio:
        ap = ArgsProcessor()
        ap.process()
        mockio.assert_output_contains('--help\n')
    # command, flag, param are available in autocompletions
    with MockIO(['--bash-autocomplete', 'dupa ']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('command')
        ap.add_flag('flag1')
        ap.add_flag('--flag2')
        ap.add_param('param1')
        ap.add_param('--param2')
        ap.process()
        mockio.assert_output_contains('command\n')
        mockio.assert_output_contains('--flag1\n')
        mockio.assert_output_contains('--flag2\n')
        mockio.assert_output_contains('--param1\n')
        mockio.assert_output_contains('--param2\n')
    # subcommands autocomplete
    with MockIO(['--bash-autocomplete', 'dupa command ']) as mockio:
        ap = ArgsProcessor()
        ap_command = ap.add_subcommand('command')
        ap_command.add_subcommand('sub2')
        ap_command.add_flag('flag1')
        ap_command.add_param('param1')
        ap.process()
        assert not mockio.output_contains('command')
        mockio.assert_output_contains('sub2\n')
        mockio.assert_output_contains('--flag1\n')
        mockio.assert_output_contains('--param1\n')
    with MockIO(['--bash-autocomplete', 'dupa com']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('command')
        ap.process()
        mockio.assert_output('command\n')
    with MockIO(['--bash-autocomplete', 'dupa c1 c2 ']) as mockio:
        ap = ArgsProcessor()
        ap.add_subcommand('c1').add_subcommand('c2').add_subcommand('c3')
        ap.process()
        assert not mockio.output_contains('c1')
        assert not mockio.output_contains('c2')
        mockio.assert_output_contains('c3\n')
        mockio.assert_output_contains('--help\n')
