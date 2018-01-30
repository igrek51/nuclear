#!/usr/bin/python
"""
glue v1.3.5
Common Utilities Toolkit compatible with Python 2.7 and 3

Author: igrek51
"""
import os
import sys
import re
import subprocess
import glob
import inspect
import time
from builtins import bytes

# ----- Coloured output
def debug(message):
    print('\033[32m\033[1m[debug]\033[0m ' + str(message))

def info(message):
    print('\033[34m\033[1m[info]\033[0m  ' + str(message))

def warn(message):
    print('\033[33m\033[1m[warn]\033[0m  ' + str(message))

def error(message):
    print('\033[31m\033[1m[ERROR]\033[0m ' + str(message))

def fatal(message):
    error(message)
    raise RuntimeError(message)

# ----- Input
def rawInput(prompt=None):
    """raw input compatible with python 2 and 3"""
    try:
       return raw_input(prompt) # python2
    except NameError:
       pass
    return input(prompt) # python3

def inputRequired(prompt):
    while True:
        inputted = rawInput(prompt)
        if not inputted:
            continue
        print
        return inputted

# ----- Shell
def shellExec(cmd):
    errCode = shellExecErrorCode(cmd)
    if errCode != 0:
        fatal('failed executing: %s' % cmd)

def shellExecErrorCode(cmd):
    return subprocess.call(cmd, shell=True)

def shellOutput(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = process.communicate()
    return output.decode('utf-8')

# ----- String Splitting
def splitLines(inputString):
    allLines = inputString.splitlines()
    return list(filter(lambda l: len(l) > 0, allLines)) # filter nonempty

def split(inputString, delimiter):
    return inputString.split(delimiter)

def splitToTuple(line, attributesCount, splitter='\t'):
    parts = line.split(splitter)
    if len(parts) != attributesCount:
        fatal('invalid split parts count (found: %d, expected: %d) in line: %s' % (len(parts), attributesCount, line))
    return tuple(parts)

def splitToTuples(linesRaw, attributesCount, splitter='\t'):
    lines = splitLines(linesRaw)
    tuples = []
    for line in lines:
        tuples.append(splitToTuple(line, attributesCount, splitter))
    return tuples

# ----- RegEx
def regexReplace(inputString, regexMatch, regexReplace):
    regexMatcher = re.compile(regexMatch)
    return regexMatcher.sub(regexReplace, inputString)

def regexMatch(inputString, regexMatch):
    regexMatcher = re.compile(regexMatch)
    return bool(regexMatcher.match(inputString))

def regexReplaceLines(lines, regexMatch, regexReplace):
    regexMatcher = re.compile(regexMatch)
    filtered = []
    for line in lines:
        line = regexMatcher.sub(regexReplace, line)
        filtered.append(line)
    return filtered

def regexFilterLines(lines, regexMatch):
    regexMatcher = re.compile(regexMatch)
    filtered = []
    for line in lines:
        if regexMatcher.match(line):
            filtered.append(line)
    return filtered

def regexSearchFile(filePath, regexMatch, groupNumber):
    regexMatcher = re.compile(regexMatch)
    with open(filePath) as f:
        for line in f:
            match = regexMatcher.match(line)
            if match:
                return match.group(groupNumber)

# ----- File operations
def readFile(filePath):
    with open(filePath, 'rb') as f:
        return f.read().decode('utf-8')

def saveFile(filePath, content):
    f = open(filePath, 'wb')
    f.write(bytes(content, 'utf-8'))
    f.close()

def fileExists(path):
    return os.path.isfile(path)

def listDir(path):
    return sorted(os.listdir(path))

def setWorkdir(workdir):
    os.chdir(workdir)

def getWorkdir():
    return os.getcwd()

def getScriptRealDir():
    return os.path.dirname(os.path.realpath(__file__))

# ----- Time format operations
def str2time(timeRaw, pattern):
    """pattern: %H:%M:%S, %d.%m.%Y"""
    try:
        return time.strptime(timeRaw, pattern)
    except ValueError as e:
        return None

def time2str(datetime, pattern):
    """pattern: %H:%M:%S, %d.%m.%Y"""
    if not datetime:
        return None
    return time.strftime(pattern, datetime)

# ----- Collections helpers - syntax reminders
def filterList(condition, lst):
    # condition example: lambda l: len(l) > 0
    return list(filter(condition, lst))

def mapList(mapper, lst):
    # mapper example: lambda l: l + l
    return list(map(mapper, lst))

# ----- CLI arguments rule
class CommandArgRule:
    def __init__(self, isOption, action, syntax, description, syntaxSuffix):
        self.isOption = isOption
        self.action = action
        # store syntaxes list
        if not syntax:
            self.syntaxs = None
        elif isinstance(syntax, list):
            self.syntaxs = syntax
        else:
            self.syntaxs = [syntax]
        self.description = description
        self.syntaxSuffix = syntaxSuffix

    def _displaySyntaxPrefix(self):
        return ', '.join(self.syntaxs) if self.syntaxs else ''

    def displaySyntax(self):
        syntax = self._displaySyntaxPrefix()
        if self.syntaxSuffix:
            syntax += self.syntaxSuffix if self.syntaxSuffix[0] == ' ' else ' ' + self.syntaxSuffix
        return syntax

    def displayHelp(self, syntaxPadding):
        dispHelp = self.displaySyntax()
        if self.description:
            dispHelp = dispHelp.ljust(syntaxPadding) + ' - ' + self.description
        return dispHelp

# ----- CLI arguments parser
class ArgsProcessor:
    def __init__(self, appName, version):
        self._appName = appName
        self._version = version
        self._argsQue = sys.argv[1:] # CLI arguments list
        self._argsOffset = 0
        self.clear()
        # bind default options: help, version
        self.bindOption(printHelp, ['-h', '--help'], description='display this help and exit')
        self.bindOption(printVersion, ['-v', '--version'], description='print version')

    def clear(self):
        # default action invoked when no command nor option is recognized or when arguments list is empty
        self._defaultAction = None
        self._argRules = []
        self._params = {}
        self._flags = []
        return self

    def bindDefaultAction(self, action, description=None, syntaxSuffix=None):
        """bind action when no command nor option is recognized or argments list is empty"""
        self._defaultAction = CommandArgRule(False, action, None, description, syntaxSuffix)
        return self

    def bindCommand(self, action, syntax, description=None, syntaxSuffix=None):
        """bind action to a command. Command is processed after all the options."""
        self._argRules.append(CommandArgRule(False, action, syntax, description, syntaxSuffix))
        return self

    def bindOption(self, action, syntax, description=None, syntaxSuffix=None):
        """bind action to an option. Options are processed first (before commands)."""
        self._argRules.append(CommandArgRule(True, action, syntax, description, syntaxSuffix))
        return self

    def bindParam(self, paramName, syntax, description=None):
        return self.bindOption(lambda: self.pollParam(paramName), syntax, description, '<%s>' % paramName)

    def bindFlag(self, flagName, syntax=None, description=None):
        if flagName and not syntax:
            if len(flagName) == 1:
                syntax = '-%s' % flagName
            else:
                syntax = '--%s' % flagName
        return self.bindOption(lambda: self.setFlag(flagName), syntax, description)

    # Getting args
    def pollNext(self):
        """return next arg and remove"""
        if not self.hasNext():
            return None
        nextArg = self._argsQue[self._argsOffset]
        del self._argsQue[self._argsOffset]
        return nextArg

    def peekNext(self):
        """return next arg"""
        if not self.hasNext():
            return None
        return self._argsQue[self._argsOffset]

    def hasNext(self):
        if not self._argsQue:
            return False
        return len(self._argsQue) > self._argsOffset

    def pollNextRequired(self, paramName):
        param = self.pollNext()
        if not param:
            fatal('no %s parameter given' % paramName)
        return param

    def pollRemaining(self):
        ending = self._argsQue[self._argsOffset:]
        self._argsQue = self._argsQue[:self._argsOffset]
        return ending

    def pollRemainingJoined(self, joiner=' '):
    	return joiner.join(self.pollRemaining())

    # Processing args
    def processAll(self):
        # process the options first
        self.processOptions()
        # if left arguments list is empty
        if not self._argsQue:
            if self._defaultAction: # run default action
                self._invokeDefaultAction()
            else: # help by default
                self.printHelp()
        else:
            self._processCommands()

    def _processCommands(self):
        self._argsOffset = 0
        # recognize first arg as command
        nextArg = self.peekNext()
        rule = self._findCommandArgRule(nextArg)
        if rule:
            self.pollNext()
            self._invokeAction(rule.action)
        # if not recognized - run default action
        elif self._defaultAction:
            # run default action without removing arg
            self._invokeDefaultAction()
        else:
            fatal('unknown argument: %s' % nextArg)
        # if some args left
        if self.hasNext():
            warn('too many arguments: %s' % self.pollRemainingJoined())

    def processOptions(self):
        self._argsOffset = 0
        while self.hasNext():
            nextArg = self.peekNext()
            rule = self._findCommandArgRule(nextArg)
            if rule and rule.isOption:
                # remove arg from list
                self.pollNext()
                # process option action
                self._invokeAction(rule.action)
            else:
                # skip it - it's not the option
                self._argsOffset += 1

    def _invokeAction(self, action):
        if action is not None:
            # execute action(self) or action()
            (args, _, _, _) = inspect.getargspec(action)
            if args:
                action(self)
            else:
                action()

    def _invokeDefaultAction(self):
        rule = self._defaultAction
        self._invokeAction(rule.action)

    def _findCommandArgRule(self, arg):
        for rule in self._argRules:
            if arg in rule.syntaxs:
                return rule

    # setting / getting params
    def setParam(self, name, value):
        self._params[name] = value

    def pollParam(self, name):
        param = self.pollNextRequired(name)
        self.setParam(name, param)

    def getParam(self, name):
        return self._params.get(name, None)

    # setting / getting flags
    def setFlag(self, name):
        if name not in self._flags:
            self._flags.append(name)

    def isFlag(self, name):
        return name in self._flags

    # autogenerating help output
    def _optionRulesCount(self):
        return sum(1 for rule in self._argRules if rule.isOption)

    def _commandRulesCount(self):
        return sum(1 for rule in self._argRules if not rule.isOption)

    def _calcMinSyntaxPadding(self):
        minSyntaxPadding = 0
        for rule in self._argRules:
            syntax = rule.displaySyntax()
            if len(syntax) > minSyntaxPadding: # min padding = max from len(syntax)
                minSyntaxPadding = len(syntax)
        return minSyntaxPadding

    def printHelp(self):
        # autogenerate help
        self.printVersion()
        # print main usage
        usageSyntax = sys.argv[0]
        optionsCount = self._optionRulesCount()
        commandsCount = self._commandRulesCount()
        if optionsCount > 0:
            usageSyntax += ' [options]'
        if commandsCount > 0:
            usageSyntax += ' <command>'
        if commandsCount == 0 and self._defaultAction and self._defaultAction.syntaxSuffix: # only default rule
            usageSyntax += self._defaultAction.displaySyntax()
        print('\nUsage:\n  %s' % usageSyntax)
        # description for default action
        if self._defaultAction and self._defaultAction.description: # only default rule
            print('\n%s' % self._defaultAction.description)
        # command and options help
        syntaxPadding = self._calcMinSyntaxPadding()
        if commandsCount > 0:
            print('\nCommands:')
            for rule in self._argRules:
                if not rule.isOption:
                    print('  %s' % rule.displayHelp(syntaxPadding))
        if optionsCount > 0:
            print('\nOptions:')
            for rule in self._argRules:
                if rule.isOption:
                    print('  %s' % rule.displayHelp(syntaxPadding))
        sys.exit(0)

    def printVersion(self):
        print('%s v%s' % (self._appName, self._version))

# commands available to invoke (workaround for invoking by function reference)
def printHelp(argsProcessor):
    argsProcessor.printHelp()

def printVersion(argsProcessor):
    argsProcessor.printVersion()
    sys.exit(0)
