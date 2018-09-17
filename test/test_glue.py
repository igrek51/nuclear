# -*- coding: utf-8 -*-
from mock import patch

from glue import *

# import StringIO (Python 2 and 3 compatible)
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def assert_error(action, expected_error=None):
    try:
        action()
        assert False
    except RuntimeError as e:
        if expected_error:
            assert str(e) == expected_error


def assert_system_exit(action):
    try:
        action()
        assert False
    except SystemExit as e:
        # exit with error code 0
        assert str(e) == '0'


class MockIO:
    def __init__(self, in_args_list):
        if not in_args_list:
            in_args_list = []
        self.in_args_list = in_args_list

    def __enter__(self):
        self._mock_args = patch.object(sys, 'argv', ['glue'] + self.in_args_list)
        self._mock_output = patch('sys.stdout', new=StringIO())
        return self

    def __exit__(self, type, value, traceback):
        self._mock_args.exit(type, value, traceback)
        self._mock_output.exit(type, value, traceback)

    def output(self):
        return self._mock_output.getvalue()

    def output_contains(self, in_str):
        return in_str in self._mock_output.getvalue()


def mock_args(args_list):
    if not args_list:
        args_list = []
    return patch.object(sys, 'argv', ['glue'] + args_list)


def mock_output():
    return patch('sys.stdout', new=StringIO())


def test_output():
    with mock_output() as out:
        debug('message')
        assert 'message' in out.getvalue()
        assert 'debug' in out.getvalue()
        info('message')
        assert 'info' in out.getvalue()
        warn('message')
        assert 'warn' in out.getvalue()
        error('message')
        assert 'ERROR' in out.getvalue()
        info(7)
        assert '7' in out.getvalue()


def test_fatal():
    assert_error(lambda: fatal('fatality'))
    assert_error(lambda: fatal('fatality'), 'fatality')
    assert_system_exit(lambda: exit_now('farewell'))
    assert_system_exit(lambda: exit_now())


def test_shellExec():
    shell('echo test')
    assert_error(lambda: shell('dupafatality'))
    assert shell_error_code('echo test') == 0
    assert shell_output('echo test') == 'test\n'
    assert shell_output('echo żółć') == u'żółć\n'
    assert shell_output('echo test', as_bytes=True) == b'test\n'
    assert shell_output('echo test', as_bytes=True) == 'test\n'.encode('utf-8')
    assert shell_output('echo test', as_bytes=True).decode('utf-8') == 'test\n'


def test_splitLines():
    assert split_lines('a\nb\nc') == ['a', 'b', 'c']
    assert split_lines('\na\n\n') == ['a']
    assert split_lines('\n\n\n') == []
    assert split_lines('') == []
    assert split_lines('a\n\n\r\nb') == ['a', 'b']


def test_splitToTuple():
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


def test_splitToTuples():
    assert split_to_tuples('a\tb\tc\nd\te\tf', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('\n\na\tb\tc\n\nd\te\tf\n', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples('a\tb\tc', 3) == [('a', 'b', 'c')]
    # splitted list as input
    assert split_to_tuples(['a\tb\tc', 'd\te\tf'], 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert split_to_tuples(['a\tb\tc'], 3) == [('a', 'b', 'c')]


def test_regexReplace():
    assert regex_replace('abca', 'a', 'b') == 'bbcb'
    assert regex_replace('abc123a', r'\d', '5') == 'abc555a'


def test_regexMatch():
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


def test_input():
    sys.stdin = open('test/res/inputs')
    assert input_string() == 'in1'
    assert input_string('prompt') == 'in2'


def test_inputRequired():
    sys.stdin = open('test/res/inputRequired')
    assert input_required('required: ') == 'valid'


def test_readFile():
    assert read_file('test/res/readme') == 'Readme\n123'


def test_saveFile():
    save_file('test/res/saveme', 'dupa\n123')
    assert read_file('test/res/saveme') == 'dupa\n123'
    save_file('test/res/saveme', '')
    assert read_file('test/res/saveme') == ''


def test_listDir():
    assert list_dir('test/res/listme') == ['afile', 'dir', 'zlast', 'zlastdir']


def test_workdir():
    workdir = get_workdir()
    set_workdir('/')
    assert get_workdir() == '/'
    set_workdir('/home/')
    assert get_workdir() == '/home'
    set_workdir(workdir)


def test_getScriptRealDir():
    realDirExpected = get_workdir()
    assert script_real_dir() == realDirExpected


def test_fileExists():
    assert file_exists('test/res/readme')
    assert not file_exists('test/res/dupadupa')


def test_filterList():
    assert filter_list(lambda e: len(e) <= 3, ['a', '123', '12345']) == ['a', '123']


def test_mapList():
    assert map_list(lambda e: e + e, ['a', '123', '']) == ['aa', '123123', '']


def test_timeConversions():
    pattern = '%H:%M:%S, %d.%m.%Y'
    sampleDate = '16:26:01, 20.12.2017'
    badDate = '16:26:01 20.12.17dupa'
    datetime = str2time(sampleDate, pattern)
    assert datetime is not None
    assert time2str(datetime, pattern) == sampleDate
    assert str2time(badDate, pattern) is None
    assert time2str(None, pattern) is None


# _CommandArgRule
def test_CommandArgRule():
    assert CommandArgRule(True, None, 'name', 'description', 'syntaxSuffix')._display_syntax_prefix() == 'name'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description',
                          'syntaxSuffix')._display_syntax_prefix() == 'name1, name2'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description', None).display_syntax() == 'name1, name2'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description',
                          '<suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description',
                          ' <suffix>').display_syntax() == 'name1, name2 <suffix>'
    assert CommandArgRule(True, None, ['name'], 'description', None).display_help(5) == 'name  - description'
    assert CommandArgRule(True, None, ['name'], 'description', None).display_help(3) == 'name - description'
    assert CommandArgRule(True, None, ['name'], 'description', '<suffix>').display_help(
        3) == 'name <suffix> - description'
    assert CommandArgRule(True, None, ['name'], 'description', '<s>').display_help(10) == 'name <s>   - description'


# ArgsProcessor
def command1():
    print('None')


def commandDupa():
    print('dupa')


def command2(argsProcessor):
    param = argsProcessor.poll_next('param')
    print(param)
    return param


def command3(argsProcessor):
    param = argsProcessor.peek_next()
    if not param:
        assert not argsProcessor.has_next()
    param2 = argsProcessor.poll_next()
    assert param == param2
    print(param)


def command4Remaining(argsProcessor):
    print(argsProcessor.poll_remaining_joined())


def commandpollRemaining(argsProcessor):
    print(argsProcessor.poll_remaining())


def command5Poll(argsProcessor):
    while (argsProcessor.has_next()):
        print(argsProcessor.poll_next())


def command6SetPara(argsProcessor):
    para = argsProcessor.poll_next('para')
    argsProcessor.set_param('para', para)


def commandPrintVersionOnly(argsProcessor):
    argsProcessor.print_version()


def actionIsForce(argsProcessor):
    print('force is: ' + str(argsProcessor.is_flag_set('force')))


def actionIsF(argsProcessor):
    print('force is: ' + str(argsProcessor.is_flag_set('f')))


def sampleProcessor1():
    argsProcessor = ArgsProcessor('appName', '1.0.1')
    argsProcessor.bind_command(command1, 'command1', description='description1')
    argsProcessor.bind_command(command2, ['command2', 'command22'], description='description2', suffix='<param>')
    argsProcessor.bind_command(command3, ['command3', 'command33'], description='description2', suffix='<param>')
    argsProcessor.bind_command(command4Remaining, 'remain', description='description4', suffix='<param>')
    argsProcessor.bind_command(command5Poll, 'poll', description='description5')
    argsProcessor.bind_option(command4Remaining, '--remain', description='join strings')
    argsProcessor.bind_option(commandPrintVersionOnly, '-v2')
    argsProcessor.bind_command(command6SetPara, '--set-para', description='set para')
    argsProcessor.bind_param('para', '--para', 'set para')
    return argsProcessor


def test_ArgsProcessor_noArg():
    # basic execution with no args
    with mock_args(None):
        # prints help and exit
        assert_system_exit(lambda: ArgsProcessor('appName', '1.0.1').process_all())


def test_ArgsProcessor_bindingsSetup():
    # test bindings setup
    with mock_args(None):
        sampleProcessor1()


def test_ArgsProcessor_bindDefaultAction():
    # test bindings
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_default_action(command1).process_all()
        assert out.getvalue() == 'None\n'
    with mock_args(['-h']), mock_output() as out:
        assert_system_exit(lambda: sampleProcessor1().bind_default_action(command1).process_all())
    # rebinding
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_default_action(command1).bind_default_action(commandDupa).process_all()
        assert out.getvalue() == 'dupa\n'


def test_ArgsProcessor_bindDefaultAction():
    # test bindings
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_default_action(command1).process_all()
        assert out.getvalue() == 'None\n'


def test_ArgsProcessor_optionsFirst():
    # test processing options first
    with mock_args(['-h', 'dupa']):
        # prints help and exit
        assert_system_exit(lambda: sampleProcessor1().process_all())


def test_ArgsProcessor_noNextArg():
    # test lack of next argument
    with mock_args(['command2']), mock_output() as out:
        sampleProcessor1().process_all()
        assert 'ERROR' in out.getvalue()
        assert 'no param given' in out.getvalue()
    with mock_args(['command33']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == 'None\n'


def test_ArgsProcessor_givenParam():
    # test given param
    with mock_args(['command3', 'dupa']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == 'dupa\n'
    with mock_args(['command2', 'dupa']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == 'dupa\n'


def test_ArgsProcessor_binding():
    # test binding with no argProcessor
    with mock_args(['command1']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == 'None\n'


def test_ArgsProcessor_pollRemainingJoined():
    # test pollRemainingJoined():
    with mock_args(['remain']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == '\n'
    with mock_args(['remain', '1']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == '1\n'
    with mock_args(['remain', '1', 'abc', 'd']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == '1 abc d\n'


def test_ArgsProcessor_pollRemaining():
    with mock_args(['remaining', 'jasna', 'dupa']), mock_output() as out:
        sampleProcessor1().bind_default_action(commandpollRemaining).process_all()
        assert out.getvalue() == "['remaining', 'jasna', 'dupa']\n"


def test_ArgsProcessor_optionsPrecedence():
    # test options precedence
    with mock_args(['-v2', 'command1']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == 'appName v1.0.1\nNone\n'
    with mock_args(['--remain', '1', 'abc']), mock_output() as out:
        sampleProcessor1().bind_default_action(None).process_all()
        assert out.getvalue() == '1 abc\n'
    with mock_args(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == '1 abc\njasna dupa\n'
    with mock_args(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mock_output() as out:
        sampleProcessor1().process_options()
        assert out.getvalue() == '1 abc\n'


def test_ArgsProcessor_poll():
    # test polling
    with mock_args(['poll', '123', '456', '789']), mock_output() as out:
        sampleProcessor1().process_all()
        assert out.getvalue() == '123\n456\n789\n'


def test_ArgsProcessor_removingArgs():
    # test removing parameters
    with mock_args(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.process_options()
        argsProcessor.process_options()
        argsProcessor.process_options()
        assert out.getvalue() == '1 abc\n'
    with mock_args(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.process_options()
        argsProcessor.process_all()
        assert out.getvalue() == '1 abc\njasna dupa\n'


def test_ArgsProcessor_unknownArg():
    # test unknown argument
    with mock_args(['dupa']), mock_output() as out:
        sampleProcessor1().process_all()
        assert 'unknown argument: dupa' in out.getvalue()


def test_ArgsProcessor_defaultAction():
    with mock_args(['dupa']), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bind_default_action(command2, description='defaultAction', suffix='<param>')
        argsProcessor.process_all()
        assert out.getvalue() == 'dupa\n'
    with mock_args(None), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bind_default_action(command1, description='defaultAction', suffix='<param>')
        argsProcessor.process_all()
        assert out.getvalue() == 'None\n'
    with mock_args(None), mock_output() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bind_default_action(print_help, description='defaultAction', suffix='<param>')
        assert_system_exit(lambda: argsProcessor.process_all())
        assert '<param>' in out.getvalue()
        assert 'defaultAction' in out.getvalue()
    # test getting params
    with mock_args(['dupa2']), mock_output() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bind_default_action(command2, description='defaultAction', suffix='<param>')
        argsProcessor.process_all()
        assert out.getvalue() == 'dupa2\n'


def test_ArgsProcessor_bindDefaultOptions():
    with mock_args(['-v']), mock_output() as out:
        assert_system_exit(lambda: ArgsProcessor('appName', '1.0.1').process_all())
        assert out.getvalue() == 'appName v1.0.1\n'
    with mock_args(['-v', '-v']), mock_output() as out:
        assert_system_exit(lambda: ArgsProcessor('appName', '1.0.1').process_all())
        assert out.getvalue() == 'appName v1.0.1\n'
    with mock_args(['-h']), mock_output() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        assert_system_exit(lambda: argsProcessor.process_all())


def test_ArgsProcessor_settingParams():
    with mock_args(['--para', 'dup']), mock_output() as out:
        argsProcessor = sampleProcessor1().bind_default_action(None)
        argsProcessor.process_all()
        assert argsProcessor.get_param('para') == 'dup'
    with mock_args(['--set-para', 'dup']), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.process_all()
        assert argsProcessor.get_param('para') == 'dup'


def actionSetObjectParam(argsProcessor):
    argsProcessor.set_param('liczba', int(7))


def test_ArgsProcessor_objectParams():
    with mock_args(None), mock_output() as out:
        argsProcessor = sampleProcessor1().bind_default_action(actionSetObjectParam)
        argsProcessor.process_all()
        assert not argsProcessor.is_param('dupa')
        assert argsProcessor.get_param('dupa') is None
        assert argsProcessor.is_param('liczba')
        assert argsProcessor.get_param('liczba') is 7


def test_ArgsProcessor_optionsAndDefaultAcction():
    with mock_args(['-v2', '-v2']), mock_output() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bind_option(commandPrintVersionOnly, '-v2')
        argsProcessor.bind_default_action(command1, description='defaultAction', suffix='<param>')
        argsProcessor.process_all()
        assert out.getvalue() == 'appName v1.0.1\nappName v1.0.1\nNone\n'


def test_ArgsProcessor_toomanyargs():
    with mock_args(['command1', 'two', 'much']), mock_output() as out:
        sampleProcessor1().process_all()
        output = out.getvalue()
        assert 'None' in output
        assert 'too many arguments: two much' in output


def test_ArgsProcessor_defaultActionNone():
    with mock_args(None), mock_output() as out:
        sampleProcessor1().clear().bind_default_action(None).process_all()
        assert out.getvalue() == ''
    with mock_args(None), mock_output() as out:
        assert_system_exit(lambda: sampleProcessor1().clear().process_all())


def test_ArgsProcessor_bindFlag():
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_flag('force').bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: False\n'
    with mock_args(['--force']), mock_output() as out:
        sampleProcessor1().bind_flag('force').bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: True\n'
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_flag('force', '--for').bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: False\n'
    with mock_args(['--for']), mock_output() as out:
        sampleProcessor1().bind_flag('force', '--for').bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: True\n'
    # single letter
    with mock_args(None), mock_output() as out:
        sampleProcessor1().bind_flag('f').bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: False\n'
    with mock_args(['-f']), mock_output() as out:
        sampleProcessor1().bind_flag('f').bind_default_action(actionIsF).process_all()
        assert out.getvalue() == 'force is: True\n'
    with mock_args(['-f']), mock_output() as out:
        sampleProcessor1().bind_flag('force', ['-f', '--force']).bind_default_action(actionIsForce).process_all()
        assert out.getvalue() == 'force is: True\n'


def actionPrintParam(ap):
    print('param is: %s' % ap.get_param('param'))
    print('p is: %s' % ap.get_param('p'))


def test_ArgsProcessor_bindParam():
    with mock_args(None), mock_output() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bind_param('param', description='set param').bind_default_action(actionPrintParam).process_all()
        assert 'param is: None\n' in out.getvalue()
    with mock_args(['--param', 'dupa']), mock_output() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bind_param('param', description='set param').bind_default_action(actionPrintParam).process_all()
        assert 'param is: dupa\n' in out.getvalue()
    with mock_args(['--parameter', 'dupa']), mock_output() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bind_param('param', keywords='--parameter', description='set param').bind_default_action(
            actionPrintParam).process_all()
        assert 'param is: dupa\n' in out.getvalue()
    # single letter
    with mock_args(None), mock_output() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bind_param('p', description='set param').bind_default_action(actionPrintParam).process_all()
        assert 'p is: None\n' in out.getvalue()
    with mock_args(['-p', 'dupa']), mock_output() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bind_param('p', description='set param').bind_default_action(actionPrintParam).process_all()
        assert 'p is: dupa\n' in out.getvalue()


def actionPrintFromTo(argsProcessor):
    print('range: ' + argsProcessor.get_param('fromDate') + ' - ' + argsProcessor.get_param('toDate'))


def test_ArgsProcessor_2params():
    with mock_args(['print', '--from', 'today', '--to', 'tomorrow']), mock_output() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bind_param('fromDate', keywords='--from')
        argsProcessor.bind_param('toDate', keywords='--to')
        argsProcessor.bind_command(actionPrintFromTo, 'print')
        argsProcessor.process_all()
        assert 'range: today - tomorrow' in out.getvalue()


def actionGetParam(ap):
    print(ap.get_param('musthave', required=True))


def test_getMissingRequiredParam():
    with mock_args([]), mock_output() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bind_param('musthave')
        argsProcessor.bind_default_action(actionGetParam)
        argsProcessor.process_all()
        assert 'no required param given: musthave' in out.getvalue()
