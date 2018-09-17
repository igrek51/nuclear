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


# ----- Input -----
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


# ----- Shell -----
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


# ----- String Splitting -----
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


# ----- RegEx -----
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


# ----- File, directories operations -----
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


# ----- Time format converters -----
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


# ----- Collections helpers - syntax reminders -----
def filter_list(condition, lst):
    # condition example: lambda l: len(l) > 0
    return list(filter(condition, lst))


def map_list(mapper, lst):
    # mapper example: lambda l: l + l
    return list(map(mapper, lst))


# ----- CLI arguments rule -----
class CliArgRule(object):
    def __init__(self, keywords=None, description=None, syntax=None, completer=None,
                 completer_choices=None):
        """
        :param keywords: triggering keyword / keywords - string or list of string
        :param description: description of action to show in help
        :param syntax: syntax of action to show in help
        :param completer: auto completer - possible choices generator
        :param completer_choices: list of possible choices
        """
        self.help = description
        self.syntax = syntax
        self.completer = completer
        self.completer_choices = completer_choices
        # store keywords list
        if not keywords:
            self.keywords = None
        elif isinstance(keywords, list):
            self.keywords = keywords
        else:  # keyword as single string
            self.keywords = [keywords]

    def _display_syntax_prefix(self):
        return ', '.join(self.keywords) if self.keywords else ''

    def display_syntax(self):
        syntax_out = self._display_syntax_prefix()
        if self.syntax:
            syntax_out += self.syntax if self.syntax[0] == ' ' else ' ' + self.syntax
        return syntax_out

    def display_syntax_max_length(self):
        return len(self.display_syntax())

    def display_help(self, syntax_padding):
        display_help_out = self.display_syntax()
        if self.help:
            display_help_out = display_help_out.ljust(syntax_padding) + ' - ' + self.help
        return display_help_out


class CommandArgRule(CliArgRule):
    def __init__(self, action, subparser, **kwargs):
        """
        :param keywords:
        :param action: action to execute when triggered
        :param description:
        :param syntax:
        :param completer:
        :param completer_choices:
        :param subparser:
        """
        super(CommandArgRule, self).__init__(**kwargs)
        self.subparser = subparser
        self.action = action

    def display_syntax_max_length(self):
        subrules = self.subparser._rules_params + self.subparser._rules_flags + self.subparser._rules_commands
        max_length = super(CommandArgRule, self).display_syntax_max_length()
        for rule in subrules:
            length = rule.display_syntax_max_length()
            if length > max_length:
                max_length = length
        return max_length


class ParamArgRule(CliArgRule):
    def __init__(self, name, required, **kwargs):
        super(ParamArgRule, self).__init__(**kwargs)
        self.name = name
        self.required = required


class FlagArgRule(CliArgRule):
    def __init__(self, name, **kwargs):
        super(FlagArgRule, self).__init__(**kwargs)
        self.name = name


# ----- CLI arguments parser -----
class CliSyntaxError(RuntimeError):
    pass


class SubArgsProcessor(object):
    def __init__(self, default_action=None, parent=None):
        self._default_action = default_action
        self.parent = parent
        self._rules_params = []
        self._rules_flags = []
        self._rules_commands = []
        self._params = {}
        self._flags = []
        self._args_que = None
        self._argsOffset = None

    def add_subcommand(self, keywords, action=None, description=None, syntax=None, completer=None,
                       completer_choices=None):
        """
        Bind command keyword to an action. Command is processed after all params and flags.
        It creates a sub-command processor to handle command specific params, flags or next level sub-commands.
        :param keywords: trigger name or names (string or list of strings)
        :param action: action to invoke when triggered
        :param description: description of action to show in help
        :param syntax: syntax of action to show in help
        :param completer: auto completer - possible choices generator
        :param completer_choices: list of possible choices
        :return: next level subparser (with command context)
        """
        # create subparser
        subparser = SubArgsProcessor(default_action=action, parent=self)
        self._rules_commands.append(
            CommandArgRule(action=action, subparser=subparser, keywords=keywords, description=description,
                           syntax=syntax, completer=completer, completer_choices=completer_choices))
        return subparser

    def add_param(self, name=None, keywords=None, description=None, completer=None, completer_choices=None,
                  required=False):
        """
        Add parameter to retrieve later on. Syntax: '--param value' or '--param=value'
        :param name: param name
        :param keywords: trigger name or names (string or list of strings)
        :param description: description of param to show in help
        :param completer: auto completer - possible choices generator
        :param completer_choices: list of possible choices
        :param required: is param required
        :return: this parser
        """
        if name and not keywords:  # complete keyword if not given
            keywords = self._get_keyword_from_name(name)
        if name:
            syntax = '[%s]' % name
        self._rules_params.append(
            ParamArgRule(name=name, required=required, keywords=keywords, description=description, completer=completer,
                         completer_choices=completer_choices, syntax=syntax))
        return self

    def add_flag(self, name, keywords=None, description=None):
        """
        Add flag to check later on. Syntax: '--flag', '-f'
        :param name: flag name
        :param keywords: trigger name or names (string or list of strings)
        If missing, keywords will be autogenerated (--name or -n)
        :param description: description of flag to show in help
        :return: this parser
        """
        if name and not keywords:  # complete keyword if not given
            keywords = self._get_keyword_from_name(name)
        self._rules_flags.append(FlagArgRule(name=name, keywords=keywords, description=description))
        return self

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
        next_arg = self._args_que[self._argsOffset]
        del self._args_que[self._argsOffset]
        return next_arg

    def peek_next(self):
        """return next arg"""
        if not self.has_next():
            return None
        return self._args_que[self._argsOffset]

    def has_next(self):
        if not self._args_que:
            return False
        return len(self._args_que) > self._argsOffset

    def poll_remaining(self):
        ending = self._args_que[self._argsOffset:]
        self._args_que = self._args_que[:self._argsOffset]
        return ending

    def poll_remaining_joined(self, joiner=' '):
        return joiner.join(self.poll_remaining())

    # Processing args
    def process(self):
        try:
            # CLI arguments list skipping executable name
            self.process_args(sys.argv[1:])
        except CliSyntaxError as e:
            error('Wrong command line syntax: %s' % str(e))

    def process_args(self, args):
        self._args_que = args
        self._argsOffset = 0
        # process the flags and params first
        self._process_flags()
        self._process_params()
        # if there's no arguments left
        if not self._args_que:
            # no command to invoke - run default action
            if self._default_action:
                self._invoke_action(self._default_action)
        else:
            self._process_commands()

    def _process_flags(self):
        self._argsOffset = 0
        while self.has_next():
            next_arg = self.peek_next()
            rule = self._find_rule_by_keyword(self._rules_flags, next_arg)
            if rule:
                # remove arg from list
                self.poll_next()
                # save flag is set
                self.set_flag(rule.name)
            else:
                # skip it - it's not what we're looking for
                self._argsOffset += 1

    def _process_params(self):
        self._argsOffset = 0
        processed_params = []
        while self.has_next():
            next_arg = self.peek_next()
            rule = self._process_param(next_arg)
            if rule:
                # mark param was processed
                processed_params.append(rule)
            else:
                # skip it - it's not what we're looking for
                self._argsOffset += 1
        # check for unprocessed required params
        unprocessed = filter(lambda r: r.required and r not in processed_params, self._rules_params)
        unprocessed = map(lambda r: r.name, unprocessed)
        if unprocessed:
            raise CliSyntaxError('The following missing params are required: %s' % ', '.join(unprocessed))

    def _process_commands(self):
        self._argsOffset = 0
        # recognize first arg as command
        next_arg = self.peek_next()
        rule = self._find_rule_by_keyword(self._rules_commands, next_arg)
        if rule:  # if found a command
            self.poll_next()
            # pass all retrieved params and flags
            rule.subparser._params = self._params
            rule.subparser._flags = self._flags
            # pass all remaining args to subparser
            remaining_args = self.poll_remaining()
            rule.subparser.process_args(remaining_args)
        # if not recognized - run default action
        elif self._default_action:
            # run default action without removing args
            self._invoke_action(self._default_action)
        else:
            raise CliSyntaxError('unknown command: %s' % next_arg)
        # if some args left
        if self.has_next():
            warn('redundant arguments: %s' % self.poll_remaining_joined(' '))

    def _invoke_action(self, action):
        if action is not None:
            # execute action(self) or action()
            (args, _, _, _) = inspect.getargspec(action)
            if args:
                action(self)
            else:
                action()

    @staticmethod
    def _find_rule_by_keyword(rules, arg):
        for rule in rules:
            if arg in rule.keywords:
                return rule

    def _process_param(self, arg):
        for rule in self._rules_params:
            for keyword in rule.keywords:
                if arg == keyword:
                    # --param value
                    self.poll_next()  # --param
                    value = self.poll_next(required_name=rule.name)
                    self.set_param(rule.name, value)
                    return rule
                elif arg.startswith(keyword + '='):
                    # --param=value
                    param_with_value = self.poll_next()
                    value = param_with_value[len(keyword + '='):]
                    self.set_param(rule.name, value)
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

    def print_commands(self, command_rule, syntax_padding):
        # command help
        print('  %s' % command_rule.display_help(syntax_padding))
        # and all its children
        subrules = self._rules_commands + self._rules_flags + self._rules_params
        display_help_prefix = command_rule.display_syntax()
        for subrule in subrules:
            display_help_out = display_help_prefix + subrule.display_syntax()
            if subrule.help:
                display_help_out = display_help_out.ljust(syntax_padding) + ' - ' + subrule.help
            print('  %s' % display_help_out)


class ArgsProcessor(SubArgsProcessor):
    def __init__(self, app_name='Command Line Application', version='0.0.1', default_action=None, syntax=None):
        super(ArgsProcessor, self).__init__(default_action)
        self._appName = app_name
        self._version = version
        self._syntax = syntax
        # default action - help
        if not self._default_action:
            self._default_action = print_help
        # bind default options: help, version
        self.add_subcommand(['-h', '--help'], action=print_help, description='display this help and exit')
        self.add_subcommand(['-v', '--version'], action=print_version, description='print version')

    # auto generating help output
    def _calc_min_syntax_padding(self):
        min_syntax_padding = 0
        for rule in self._rules_flags + self._rules_params + self._rules_commands:
            syntax_length = rule.display_syntax_max_length()
            if syntax_length > min_syntax_padding:  # min padding = max from len(syntax)
                min_syntax_padding = syntax_length
        return min_syntax_padding

    def print_help(self):
        # auto generate help
        self.print_version()
        # print main usage
        usage_syntax = sys.argv[0]
        commands_count = sum(1 for _ in self._rules_commands)
        options_count = sum(1 for _ in self._rules_flags + self._rules_params)
        if options_count > 0:
            usage_syntax += ' [options]'
        if commands_count > 0:
            usage_syntax += ' <command>'
        if self._syntax:  # only default rule
            usage_syntax += self._syntax
        print('\nUsage:\n  %s' % usage_syntax)
        # commands help
        syntax_padding = self._calc_min_syntax_padding()
        if commands_count > 0:
            print('\nCommands:')
            for rule in self._rules_commands:
                rule.subparser.print_commands(rule, syntax_padding)
        # options
        if options_count > 0:
            print('\nOptions:')
            for rule in self._rules_flags + self._rules_params:
                print('  %s' % rule.display_help(syntax_padding))
        sys.exit(0)

    def print_version(self):
        print('%s v%s' % (self._appName, self._version))


# commands available to invoke (workaround for invoking by function reference)
def print_help(ap):
    if ap.parent:
        ap = ap.parent
    ap.print_help()


def print_version(ap):
    if ap.parent:
        ap = ap.parent
    ap.print_version()
    sys.exit(0)
