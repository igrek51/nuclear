"""
glue v2.0.1
One script to rule them all. - Common Utilities Toolkit compatible with both Python 2.7 and 3

Author: igrek51
"""
import datetime
import inspect
import os
import re
import subprocess
import sys
from builtins import bytes


# ----- Pretty output

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


def exit_now(message=None):
    if message:
        error(message)
    sys.exit(0)


# ----- Input
def input_string(prompt=None):
    """raw input compatible with python 2 and 3"""
    try:
        return raw_input(prompt)  # python2
    except NameError:
        pass
    return input(prompt)  # python3


def input_required(prompt):
    while True:
        inputted = input_string(prompt)
        if not inputted:
            continue
        print
        return inputted


# ----- Shell
def shell(cmd):
    err_code = shell_error_code(cmd)
    if err_code != 0:
        fatal('failed executing: %s' % cmd)


def shell_error_code(cmd):
    return subprocess.call(cmd, shell=True)


def shell_output(cmd, as_bytes=False):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = process.communicate()
    if as_bytes:
        return output
    else:
        return output.decode('utf-8')


# ----- String Splitting
def split_lines(str_in):
    all_lines = str_in.splitlines()
    return list(filter(lambda l: len(l) > 0, all_lines))  # filter nonempty


def split_to_tuple(line, attrs_count=None, splitter='\t'):
    parts = line.split(splitter)
    # attrsCount validation
    if attrs_count and len(parts) != attrs_count:
        fatal('invalid split parts count (found: %d, expected: %d) in line: %s' % (len(parts), attrs_count, line))
    return tuple(parts)


def split_to_tuples(lines, attrs_count=None, splitter='\t'):
    # lines as list or raw string
    if not isinstance(lines, list):
        lines = split_lines(lines)
    return list(map(lambda line: split_to_tuple(line, attrs_count, splitter), lines))


# ----- RegEx
def regex_match(str_in, regex_match_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return bool(regex_matcher.match(str_in))


def regex_replace(str_in, regex_match_pattern, regex_replace_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return regex_matcher.sub(regex_replace_pattern, str_in)


def regex_filter_list(lines, regex_match_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return list(filter(lambda line: regex_matcher.match(line), lines))


def regex_replace_list(lines, regex_match_pattern, regex_replace_pattern):
    regex_matcher = re.compile(regex_match_pattern)
    return list(map(lambda line: regex_matcher.sub(regex_replace_pattern, line), lines))


def regex_search_file(file_path, regex_match_pattern, group_number):
    regex_matcher = re.compile(regex_match_pattern)
    with open(file_path) as f:
        for line in f:
            match = regex_matcher.match(line)
            if match:
                return match.group(group_number)


def regex_replace_file(file_path, regex_match_pattern, regex_replace_pattern):
    file_content = read_file(file_path)
    lines = split_lines(file_content)
    lines = regex_replace_list(lines, regex_match_pattern, regex_replace_pattern)
    return '\n'.join(lines)


# ----- File, directories operations
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8')


def save_file(file_path, content):
    f = open(file_path, 'wb')
    f.write(bytes(content, 'utf-8'))
    f.close()


def file_exists(path):
    return os.path.isfile(path)


def list_dir(path):
    return sorted(os.listdir(path))


def set_workdir(work_dir):
    os.chdir(work_dir)


def get_workdir():
    return os.getcwd()


def script_real_dir():
    return os.path.dirname(os.path.realpath(__file__))


# ----- Time format converters
def str2time(time_raw, pattern):
    """pattern: %Y-%m-%d, %H:%M:%S"""
    try:
        return datetime.datetime.strptime(time_raw, pattern)
    except ValueError as _:
        return None


def time2str(date_time, pattern):
    """pattern: %Y-%m-%d, %H:%M:%S"""
    if not date_time:
        return None
    return date_time.strftime(pattern)


# ----- Collections helpers - syntax reminders
def filter_list(condition, lst):
    # condition example: lambda l: len(l) > 0
    return list(filter(condition, lst))


def map_list(mapper, lst):
    # mapper example: lambda l: l + l
    return list(map(mapper, lst))


# ----- CLI arguments rule
class CommandArgRule:
    def __init__(self, is_option, action, keywords, help_info, suffix):
        self.isOption = is_option  # should it be processed first
        self.action = action
        # store keywords list
        if not keywords:
            self.keywords = None
        elif isinstance(keywords, list):
            self.keywords = keywords
        else:  # keyword as single string
            self.keywords = [keywords]
        self.help = help_info
        self.suffix = suffix

    def _display_syntax_prefix(self):
        return ', '.join(self.keywords) if self.keywords else ''

    def display_syntax(self):
        syntax = self._display_syntax_prefix()
        if self.suffix:
            syntax += self.suffix if self.suffix[0] == ' ' else ' ' + self.suffix
        return syntax

    def display_help(self, syntax_padding):
        disp_help = self.display_syntax()
        if self.help:
            disp_help = disp_help.ljust(syntax_padding) + ' - ' + self.help
        return disp_help


# ----- CLI arguments parser
class CliSyntaxError(RuntimeError):
    pass


class ArgsProcessor:
    def __init__(self, app_name='Command Line Application', version='0.0.1'):
        self._appName = app_name
        self._version = version
        self._argsQue = sys.argv[1:]  # CLI arguments list
        self._argsOffset = 0
        self._default_action = None
        self._arg_rules = []
        self._params = {}
        self._flags = []
        # bind default options: help, version
        self.bind_option(print_help, ['-h', '--help'], help_info='display this help and exit')
        self.bind_option(print_version, ['-v', '--version'], help_info='print version')

    def clear(self):
        # default action invoked when no command nor option is recognized or when arguments list is empty
        self._default_action = None
        self._arg_rules = []
        self._params = {}
        self._flags = []
        return self

    def bind_default_action(self, action, help_info=None, suffix=None):
        """bind action when no command nor option is recognized or argments list is empty"""
        self._default_action = CommandArgRule(False, action, None, help_info, suffix)
        return self

    def bind_command(self, action, keywords, help_info=None, suffix=None):
        """bind action to a command. Command is processed after all the options."""
        self._arg_rules.append(CommandArgRule(False, action, keywords, help_info, suffix))
        return self

    def bind_option(self, action, keywords, help_info=None, suffix=None):
        """bind action to an option. Options are processed first (before commands)."""
        self._arg_rules.append(CommandArgRule(True, action, keywords, help_info, suffix))
        return self

    def bind_param(self, param_name, keywords=None, help_info=None):
        if param_name and not keywords:  # complete keyword if not given
            keywords = self._get_keyword_from_name(param_name)
        action = lambda: self.set_param(param_name, self.poll_next(param_name))
        return self.bind_option(action, keywords, help_info, suffix='<%s>' % param_name)

    def bind_flag(self, flag_name, keywords=None, help_info=None):
        if flag_name and not keywords:  # complete keyword if not given
            keywords = self._get_keyword_from_name(flag_name)
        action = lambda: self.set_flag(flag_name)
        return self.bind_option(action, keywords, help_info)

    @staticmethod
    def _get_keyword_from_name(name):
        if len(name) == 1:
            return '-%s' % name
        else:
            return '--%s' % name

    # Getting args
    def poll_next(self, required_name=None):
        """return next arg and remove"""
        if not self.has_next():
            if required_name:
                raise CliSyntaxError('no %s given' % required_name)
            return None
        next_arg = self._argsQue[self._argsOffset]
        del self._argsQue[self._argsOffset]
        return next_arg

    def peek_next(self):
        """return next arg"""
        if not self.has_next():
            return None
        return self._argsQue[self._argsOffset]

    def has_next(self):
        if not self._argsQue:
            return False
        return len(self._argsQue) > self._argsOffset

    def poll_remaining(self):
        ending = self._argsQue[self._argsOffset:]
        self._argsQue = self._argsQue[:self._argsOffset]
        return ending

    def poll_remaining_joined(self, joiner=' '):
        return joiner.join(self.poll_remaining())

    # Processing args
    def process_all(self):
        try:
            # process the options first
            self.process_options()
            # if left arguments list is empty
            if not self._argsQue:
                if self._default_action:  # run default action
                    self._invoke_default_action()
                else:  # help by default
                    self.print_help()
            else:
                self._process_commands()
        except CliSyntaxError as e:
            error('Wrong command line syntax: %s' % str(e))

    def _process_commands(self):
        self._argsOffset = 0
        # recognize first arg as command
        next_arg = self.peek_next()
        rule = self._find_command_arg_rule(next_arg)
        if rule:
            self.poll_next()
            self._invoke_action(rule.action)
        # if not recognized - run default action
        elif self._default_action:
            # run default action without removing arg
            self._invoke_default_action()
        else:
            raise CliSyntaxError('unknown argument: %s' % next_arg)
        # if some args left
        if self.has_next():
            warn('too many arguments: %s' % self.poll_remaining_joined())

    def process_options(self):
        self._argsOffset = 0
        while self.has_next():
            next_arg = self.peek_next()
            rule = self._find_command_arg_rule(next_arg)
            if rule and rule.isOption:
                # remove arg from list
                self.poll_next()
                # process option action
                self._invoke_action(rule.action)
            else:
                # skip it - it's not the option
                self._argsOffset += 1

    def _invoke_action(self, action):
        if action is not None:
            # execute action(self) or action()
            (args, _, _, _) = inspect.getargspec(action)
            if args:
                action(self)
            else:
                action()

    def _invoke_default_action(self):
        rule = self._default_action
        self._invoke_action(rule.action)

    def _find_command_arg_rule(self, arg):
        for rule in self._arg_rules:
            if arg in rule.keywords:
                return rule

    # setting / getting params
    def set_param(self, name, value):
        self._params[name] = value

    def get_param(self, name, required=False):
        if required and name not in self._params:
            raise CliSyntaxError('no required param given: %s' % name)
        return self._params.get(name, None)

    def is_param(self, name):
        return self.get_param(name) is not None

    # setting / getting flags
    def set_flag(self, name):
        if name not in self._flags:
            self._flags.append(name)

    def is_flag_set(self, name):
        return name in self._flags

    # auto generating help output
    def _option_rules_count(self):
        return sum(1 for rule in self._arg_rules if rule.isOption)

    def _command_rules_count(self):
        return sum(1 for rule in self._arg_rules if not rule.isOption)

    def _calc_min_syntax_padding(self):
        min_syntax_padding = 0
        for rule in self._arg_rules:
            syntax = rule.display_syntax()
            if len(syntax) > min_syntax_padding:  # min padding = max from len(syntax)
                min_syntax_padding = len(syntax)
        return min_syntax_padding

    def print_help(self):
        # auto generate help
        self.print_version()
        # print main usage
        usage_syntax = sys.argv[0]
        options_count = self._option_rules_count()
        commands_count = self._command_rules_count()
        if options_count > 0:
            usage_syntax += ' [options]'
        if commands_count > 0:
            usage_syntax += ' <command>'
        if commands_count == 0 and self._default_action and self._default_action.suffix:  # only default rule
            usage_syntax += self._default_action.display_syntax()
        print('\nUsage:\n  %s' % usage_syntax)
        # description for default action
        if self._default_action and self._default_action.help:  # only default rule
            print('\n%s' % self._default_action.help)
        # command and options help
        syntax_padding = self._calc_min_syntax_padding()
        if commands_count > 0:
            print('\nCommands:')
            for rule in self._arg_rules:
                if not rule.isOption:
                    print('  %s' % rule.display_help(syntax_padding))
        if options_count > 0:
            print('\nOptions:')
            for rule in self._arg_rules:
                if rule.isOption:
                    print('  %s' % rule.display_help(syntax_padding))
        sys.exit(0)

    def print_version(self):
        print('%s v%s' % (self._appName, self._version))


# commands available to invoke (workaround for invoking by function reference)
def print_help(ap):
    ap.print_help()


def print_version(ap):
    ap.print_version()
    sys.exit(0)
