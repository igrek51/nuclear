# -*- coding: utf-8 -*-
from glue import *
from mock import patch
# import StringIO (Python 2 and 3 compatible)
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def assertError(action, expectedError=None):
    try:
        action()
        assert False
    except RuntimeError as e:
        if expectedError:
            assert str(e) == expectedError

def assertSystemExit(action):
    try:
        action()
        assert False
    except SystemExit as e:
        # exit with error code 0
        assert str(e) == '0'

def mockArgs(argsList):
    if not argsList:
        argsList = []
    return patch.object(sys, 'argv', ['glue'] + argsList)

def mockOutput():
    return patch('sys.stdout', new=StringIO())


def test_output():
    with mockOutput() as out:
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
    assertError(lambda: fatal('fatality'))
    assertError(lambda: fatal('fatality'), 'fatality')
    assertSystemExit(lambda: exit('farewell'))
    assertSystemExit(lambda: exit())

def test_shellExec():
    shellExec('echo test')
    assertError(lambda: shellExec('dupafatality'))
    assert shellExecErrorCode('echo test') == 0
    assert shellOutput('echo test') == 'test\n'
    assert shellOutput('echo żółć') == u'żółć\n'
    assert shellOutput('echo test', asBytes=True) == b'test\n'
    assert shellOutput('echo test', asBytes=True) == 'test\n'.encode('utf-8')
    assert shellOutput('echo test', asBytes=True).decode('utf-8') == 'test\n'

def test_splitLines():
    assert splitLines('a\nb\nc') == ['a', 'b', 'c']
    assert splitLines('\na\n\n') == ['a']
    assert splitLines('\n\n\n') == []
    assert splitLines('') == []
    assert splitLines('a\n\n\r\nb') == ['a', 'b']

def test_splitToTuple():
    assert splitToTuple('a', 1) == ('a',)
    assert splitToTuple('', 1) == ('',)
    assertError(lambda: splitToTuple('a', 2))
    assert splitToTuple('a\tb', 2) == ('a','b')
    assertError(lambda: splitToTuple('a\tb', 1))
    assertError(lambda: splitToTuple('a\tb\t', 2))
    assert splitToTuple('a\tb\t', 3) == ('a','b','')
    assert splitToTuple('a\tb\tc', 3) == ('a','b','c')
    assert splitToTuple('a b c', 3, ' ') == ('a','b','c')
    # no attrsCount verification
    assert splitToTuple('a b c', splitter=' ') == ('a','b','c')
    assert splitToTuple('a') == ('a',)

def test_splitToTuples():
    assert splitToTuples('a\tb\tc\nd\te\tf', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert splitToTuples('\n\na\tb\tc\n\nd\te\tf\n', 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert splitToTuples('a\tb\tc', 3) == [('a', 'b', 'c')]
    # splitted list as input
    assert splitToTuples(['a\tb\tc', 'd\te\tf'], 3) == [('a', 'b', 'c'), ('d', 'e', 'f')]
    assert splitToTuples(['a\tb\tc'], 3) == [('a', 'b', 'c')]

def test_regexReplace():
    assert regexReplace('abca', 'a', 'b') == 'bbcb'
    assert regexReplace('abc123a', r'\d', '5') == 'abc555a'

def test_regexMatch():
    assert regexMatch('ab 12 def 123', r'.*\d{2}')
    assert not regexMatch('ab 1 def 1m2', r'.*\d{2}.*')

def test_regex_list():
    # regexReplaceList
    assert regexReplaceList(['a', 'b', '25', 'c'], r'\d+', '7') == ['a', 'b', '7', 'c']
    assert regexReplaceList(['a1', '2b', '3', ''], r'\d', '7') == ['a7', '7b', '7', '']
    assert regexReplaceList(['a1', '2b', '3', ''], r'.*\d.*', '7') == ['7', '7', '7', '']
    # regexFilterLines
    assert regexFilterList(['a1', '2b', '3', ''], r'.*\d.*') == ['a1', '2b', '3']
    assert regexFilterList(['a1', '2b', '3', ''], r'dupa') == []
    # regexSearchFile
    assert regexSearchFile('test/res/findme', r'\t*<author>(\w*)</author>', 1) == 'Anonim'
    assert regexSearchFile('test/res/findme', r'\t*<name>(\w*)</name><sur>(\w*)</sur>', 2) == 'Sur'
    # regexReplaceFile
    saveFile('test/res/replaceme', 'dupa\n123')
    assert regexReplaceFile('test/res/replaceme', r'[a-z]+', 'letters') == 'letters\n123'

def test_input():
    sys.stdin = open('test/res/inputs')
    assert rawInput() == 'in1'
    assert rawInput('prompt') == 'in2'

def test_inputRequired():
    sys.stdin = open('test/res/inputRequired')
    assert inputRequired('required: ') == 'valid'

def test_readFile():
    assert readFile('test/res/readme') == 'Readme\n123'

def test_saveFile():
    saveFile('test/res/saveme', 'dupa\n123')
    assert readFile('test/res/saveme') == 'dupa\n123'
    saveFile('test/res/saveme', '')
    assert readFile('test/res/saveme') == ''

def test_listDir():
    assert listDir('test/res/listme') == ['afile', 'dir', 'zlast', 'zlastdir']

def test_workdir():
    workdir = getWorkdir()
    setWorkdir('/')
    assert getWorkdir() == '/'
    setWorkdir('/home/')
    assert getWorkdir() == '/home'
    setWorkdir(workdir)

def test_getScriptRealDir():
    realDirExpected = getWorkdir()
    assert getScriptRealDir() == realDirExpected

def test_fileExists():
    assert fileExists('test/res/readme')
    assert not fileExists('test/res/dupadupa')

def test_filterList():
    assert filterList(lambda e: len(e) <= 3, ['a', '123', '12345']) == ['a', '123']

def test_mapList():
    assert mapList(lambda e: e + e, ['a', '123', '']) == ['aa', '123123', '']

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
    assert CommandArgRule(True, None, 'name', 'description', 'syntaxSuffix')._displaySyntaxPrefix() == 'name'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description', 'syntaxSuffix')._displaySyntaxPrefix() == 'name1, name2'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description', None).displaySyntax() == 'name1, name2'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description', '<suffix>').displaySyntax() == 'name1, name2 <suffix>'
    assert CommandArgRule(True, None, ['name1', 'name2'], 'description', ' <suffix>').displaySyntax() == 'name1, name2 <suffix>'
    assert CommandArgRule(True, None, ['name'], 'description', None).displayHelp(5) == 'name  - description'
    assert CommandArgRule(True, None, ['name'], 'description', None).displayHelp(3) == 'name - description'
    assert CommandArgRule(True, None, ['name'], 'description', '<suffix>').displayHelp(3) == 'name <suffix> - description'
    assert CommandArgRule(True, None, ['name'], 'description', '<s>').displayHelp(10) == 'name <s>   - description'

# ArgsProcessor
def command1():
    print('None')

def commandDupa():
    print('dupa')

def command2(argsProcessor):
    param = argsProcessor.pollNext('param')
    print(param)
    return param

def command3(argsProcessor):
    param = argsProcessor.peekNext()
    if not param:
        assert not argsProcessor.hasNext()
    param2 = argsProcessor.pollNext()
    assert param == param2
    print(param)

def command4Remaining(argsProcessor):
    print(argsProcessor.pollRemainingJoined())

def commandpollRemaining(argsProcessor):
    print(argsProcessor.pollRemaining())

def command5Poll(argsProcessor):
    while(argsProcessor.hasNext()):
        print(argsProcessor.pollNext())

def command6SetPara(argsProcessor):
    para = argsProcessor.pollNext('para')
    argsProcessor.setParam('para', para)

def commandPrintVersionOnly(argsProcessor):
    argsProcessor.printVersion()

def actionIsForce(argsProcessor):
    print('force is: ' + str(argsProcessor.isFlag('force')))

def actionIsF(argsProcessor):
    print('force is: ' + str(argsProcessor.isFlag('f')))

def sampleProcessor1():
    argsProcessor = ArgsProcessor('appName', '1.0.1')
    argsProcessor.bindCommand(command1, 'command1', help='description1')
    argsProcessor.bindCommand(command2, ['command2', 'command22'], help='description2', suffix='<param>')
    argsProcessor.bindCommand(command3, ['command3', 'command33'], help='description2', suffix='<param>')
    argsProcessor.bindCommand(command4Remaining, 'remain', help='description4', suffix='<param>')
    argsProcessor.bindCommand(command5Poll, 'poll', help='description5')
    argsProcessor.bindOption(command4Remaining, '--remain', help='join strings')
    argsProcessor.bindOption(commandPrintVersionOnly, '-v2')
    argsProcessor.bindCommand(command6SetPara, '--set-para', help='set para')
    argsProcessor.bindParam('para', '--para', 'set para')
    return argsProcessor

def test_ArgsProcessor_noArg():
    # basic execution with no args
    with mockArgs(None):
        # prints help and exit
        assertSystemExit(lambda: ArgsProcessor('appName', '1.0.1').processAll())

def test_ArgsProcessor_bindingsSetup():
    # test bindings setup
    with mockArgs(None):
        sampleProcessor1()

def test_ArgsProcessor_bindDefaultAction():
    # test bindings
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindDefaultAction(command1).processAll()
        assert out.getvalue() == 'None\n'
    with mockArgs(['-h']), mockOutput() as out:
        assertSystemExit(lambda: sampleProcessor1().bindDefaultAction(command1).processAll())
    # rebinding
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindDefaultAction(command1).bindDefaultAction(commandDupa).processAll()
        assert out.getvalue() == 'dupa\n'

def test_ArgsProcessor_bindDefaultAction():
    # test bindings
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindDefaultAction(command1).processAll()
        assert out.getvalue() == 'None\n'

def test_ArgsProcessor_optionsFirst():
    # test processing options first
    with mockArgs(['-h', 'dupa']):
        # prints help and exit
        assertSystemExit(lambda: sampleProcessor1().processAll())

def test_ArgsProcessor_noNextArg():
    # test lack of next argument
    with mockArgs(['command2']):
        assertError(lambda: sampleProcessor1().processAll(), 'no param given')
    with mockArgs(['command33']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == 'None\n'

def test_ArgsProcessor_givenParam():
    # test given param
    with mockArgs(['command3', 'dupa']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == 'dupa\n'
    with mockArgs(['command2', 'dupa']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == 'dupa\n'

def test_ArgsProcessor_binding():
    # test binding with no argProcessor
    with mockArgs(['command1']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == 'None\n'

def test_ArgsProcessor_pollRemainingJoined():
    # test pollRemainingJoined():
    with mockArgs(['remain']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == '\n'
    with mockArgs(['remain', '1']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == '1\n'
    with mockArgs(['remain', '1', 'abc', 'd']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == '1 abc d\n'

def test_ArgsProcessor_pollRemaining():
    with mockArgs(['remaining', 'jasna', 'dupa']), mockOutput() as out:
        sampleProcessor1().bindDefaultAction(commandpollRemaining).processAll()
        assert out.getvalue() == "['remaining', 'jasna', 'dupa']\n"

def test_ArgsProcessor_optionsPrecedence():
    # test options precedence
    with mockArgs(['-v2', 'command1']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == 'appName v1.0.1\nNone\n'
    with mockArgs(['--remain', '1', 'abc']), mockOutput() as out:
        sampleProcessor1().bindDefaultAction(None).processAll()
        assert out.getvalue() == '1 abc\n'
    with mockArgs(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == '1 abc\njasna dupa\n'
    with mockArgs(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mockOutput() as out:
        sampleProcessor1().processOptions()
        assert out.getvalue() == '1 abc\n'

def test_ArgsProcessor_poll():
    # test polling
    with mockArgs(['poll', '123', '456', '789']), mockOutput() as out:
        sampleProcessor1().processAll()
        assert out.getvalue() == '123\n456\n789\n'

def test_ArgsProcessor_removingArgs():
    # test removing parameters
    with mockArgs(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.processOptions()
        argsProcessor.processOptions()
        argsProcessor.processOptions()
        assert out.getvalue() == '1 abc\n'
    with mockArgs(['remain', 'jasna', 'dupa', '--remain', '1', 'abc']), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.processOptions()
        argsProcessor.processAll()
        assert out.getvalue() == '1 abc\njasna dupa\n'

def test_ArgsProcessor_unknownArg():
    # test unknown argument
    with mockArgs(['dupa']):
        assertError(lambda: sampleProcessor1().processAll(), 'unknown argument: dupa')

def test_ArgsProcessor_defaultAction():
    with mockArgs(['dupa']), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bindDefaultAction(command2, help='defaultAction', suffix='<param>')
        argsProcessor.processAll()
        assert out.getvalue() == 'dupa\n'
    with mockArgs(None), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bindDefaultAction(command1, help='defaultAction', suffix='<param>')
        argsProcessor.processAll()
        assert out.getvalue() == 'None\n'
    with mockArgs(None), mockOutput() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bindDefaultAction(printHelp, help='defaultAction', suffix='<param>')
        assertSystemExit(lambda: argsProcessor.processAll())
        assert '<param>' in out.getvalue()
        assert 'defaultAction' in out.getvalue()
    # test getting params
    with mockArgs(['dupa2']), mockOutput() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bindDefaultAction(command2, help='defaultAction', suffix='<param>')
        argsProcessor.processAll()
        assert out.getvalue() == 'dupa2\n'

def test_ArgsProcessor_bindDefaultOptions():
    with mockArgs(['-v']), mockOutput() as out:
        assertSystemExit(lambda: ArgsProcessor('appName', '1.0.1').processAll())
        assert out.getvalue() == 'appName v1.0.1\n'
    with mockArgs(['-v', '-v']), mockOutput() as out:
        assertSystemExit(lambda: ArgsProcessor('appName', '1.0.1').processAll())
        assert out.getvalue() == 'appName v1.0.1\n'
    with mockArgs(['-h']), mockOutput() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        assertSystemExit(lambda: argsProcessor.processAll())

def test_ArgsProcessor_settingParams():
    with mockArgs(['--para', 'dup']), mockOutput() as out:
        argsProcessor = sampleProcessor1().bindDefaultAction(None)
        argsProcessor.processAll()
        assert argsProcessor.getParam('para') == 'dup'
    with mockArgs(['--set-para', 'dup']), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.processAll()
        assert argsProcessor.getParam('para') == 'dup'

def actionSetObjectParam(argsProcessor):
    argsProcessor.setParam('liczba', int(7))

def test_ArgsProcessor_objectParams():
    with mockArgs(None), mockOutput() as out:
        argsProcessor = sampleProcessor1().bindDefaultAction(actionSetObjectParam)
        argsProcessor.processAll()
        assert not argsProcessor.isParam('dupa')
        assert argsProcessor.getParam('dupa') is None
        assert argsProcessor.isParam('liczba')
        assert argsProcessor.getParam('liczba') is 7

def test_ArgsProcessor_optionsAndDefaultAcction():
    with mockArgs(['-v2', '-v2']), mockOutput() as out:
        argsProcessor = sampleProcessor1()
        argsProcessor.bindOption(commandPrintVersionOnly, '-v2')
        argsProcessor.bindDefaultAction(command1, help='defaultAction', suffix='<param>')
        argsProcessor.processAll()
        assert out.getvalue() == 'appName v1.0.1\nappName v1.0.1\nNone\n'

def test_ArgsProcessor_toomanyargs():
    with mockArgs(['command1', 'two', 'much']), mockOutput() as out:
        sampleProcessor1().processAll()
        output = out.getvalue()
        assert 'None' in output
        assert 'too many arguments: two much' in output

def test_ArgsProcessor_defaultActionNone():
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().clear().bindDefaultAction(None).processAll()
        assert out.getvalue() == ''
    with mockArgs(None), mockOutput() as out:
        assertSystemExit(lambda: sampleProcessor1().clear().processAll())

def test_ArgsProcessor_bindFlag():
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindFlag('force').bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: False\n'
    with mockArgs(['--force']), mockOutput() as out:
        sampleProcessor1().bindFlag('force').bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: True\n'
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindFlag('force', '--for').bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: False\n'
    with mockArgs(['--for']), mockOutput() as out:
        sampleProcessor1().bindFlag('force', '--for').bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: True\n'
    # single letter
    with mockArgs(None), mockOutput() as out:
        sampleProcessor1().bindFlag('f').bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: False\n'
    with mockArgs(['-f']), mockOutput() as out:
        sampleProcessor1().bindFlag('f').bindDefaultAction(actionIsF).processAll()
        assert out.getvalue() == 'force is: True\n'
    with mockArgs(['-f']), mockOutput() as out:
        sampleProcessor1().bindFlag('force', ['-f', '--force']).bindDefaultAction(actionIsForce).processAll()
        assert out.getvalue() == 'force is: True\n'

def actionPrintParam(ap):
    print('param is: %s' % ap.getParam('param'))
    print('p is: %s' % ap.getParam('p'))

def test_ArgsProcessor_bindParam():
    with mockArgs(None), mockOutput() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bindParam('param', help='set param').bindDefaultAction(actionPrintParam).processAll()
        assert 'param is: None\n' in out.getvalue()
    with mockArgs(['--param', 'dupa']), mockOutput() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bindParam('param', help='set param').bindDefaultAction(actionPrintParam).processAll()
        assert 'param is: dupa\n' in out.getvalue()
    with mockArgs(['--parameter', 'dupa']), mockOutput() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bindParam('param', keywords='--parameter', help='set param').bindDefaultAction(actionPrintParam).processAll()
        assert 'param is: dupa\n' in out.getvalue()
    # single letter
    with mockArgs(None), mockOutput() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bindParam('p', help='set param').bindDefaultAction(actionPrintParam).processAll()
        assert 'p is: None\n' in out.getvalue()
    with mockArgs(['-p', 'dupa']), mockOutput() as out:
        ap = ArgsProcessor('appName', '1.0.1')
        ap.bindParam('p', help='set param').bindDefaultAction(actionPrintParam).processAll()
        assert 'p is: dupa\n' in out.getvalue()

def actionPrintFromTo(argsProcessor):
    print('range: ' + argsProcessor.getParam('fromDate') + ' - ' + argsProcessor.getParam('toDate'))

def test_ArgsProcessor_2params():
    with mockArgs(['print', '--from', 'today', '--to', 'tomorrow']), mockOutput() as out:
        argsProcessor = ArgsProcessor('appName', '1.0.1')
        argsProcessor.bindParam('fromDate', keywords='--from')
        argsProcessor.bindParam('toDate', keywords='--to')
        argsProcessor.bindCommand(actionPrintFromTo, 'print')
        argsProcessor.processAll()
        assert 'range: today - tomorrow' in out.getvalue()
