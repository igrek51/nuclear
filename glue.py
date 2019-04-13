"""
glue v2.0.11
One script to rule them all. - Common Utilities Toolkit compatible with both Python 2.7 and 3

Author: igrek51
"""
import datetime
import inspect
import os
import re
import subprocess
import sys


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


# ----- check imports -----
try:
    from builtins import bytes
except ImportError:
    error('builtins import not found, try running: "pip install future" to install missing lib')


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
    output, _ = process.communicate()
    if as_bytes:
        return output
    else:
        return output.decode('utf-8')


# ----- String Splitting -----
def nonempty_lines(str_in):
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
        lines = nonempty_lines(lines)
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
    lines = nonempty_lines(file_content)
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


def script_real_path():
    return os.path.normpath(os.path.join(script_real_dir(), sys.argv[0]))


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
    def __init__(self, keywords=None, help=None, syntax=None, choices=None):
        """
        :param keywords: triggering keyword / keywords - string or list of string
        :param help: description of action to show in help
        :param syntax: syntax of action to show in help
        :param choices: auto completer function - possible choices generator or list of possible choices
        """
        self.help = help
        self.syntax = syntax
        self.choices = choices
        # store keywords list
        if isinstance(keywords, list):
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

    def generate_choices(self, ap):
        if not self.choices:
            return []
        elif isinstance(self.choices, list):
            return self.choices
        else:
            # generator function - execute action(ap) or action()
            (args, _, _, _) = inspect.getargspec(self.choices)
            if args:
                return self.choices(ap)
            else:
                return self.choices()


class CommandArgRule(CliArgRule):
    def __init__(self, action, subparser, **kwargs):
        """
        :param keywords:
        :param action: action to execute when triggered
        :param help:
        :param syntax:
        :param completer:
        :param completer_choices:
        :param subparser:
        """
        super(CommandArgRule, self).__init__(**kwargs)
        self.subparser = subparser
        self.action = action

    def display_syntax_max_length(self):
        this_length = super(CommandArgRule, self).display_syntax_max_length()
        max_length = this_length
        subrules = self.subparser._rules_params + self.subparser._rules_flags + self.subparser._rules_commands
        for rule in subrules:
            length = rule.display_syntax_max_length() + this_length + 1
            if length > max_length:
                max_length = length
        return max_length


class PrimaryOptionRule(CliArgRule):
    def __init__(self, action, **kwargs):
        super(PrimaryOptionRule, self).__init__(**kwargs)
        self.action = action


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
        self._rules_primary_options = []
        self._params = {}
        self._flags = []
        self._args_que = None
        self._argsOffset = None

    def add_subcommand(self, keywords, action=None, help=None, syntax=None, choices=None):
        """
        Bind command keyword to an action. Command is processed after all params and flags.
        It creates a sub-command processor to handle command specific params, flags or next level sub-commands.
        :param keywords: trigger name or names (string or list of strings)
        :param action: action to invoke when triggered
        :param help: description of action to show in help
        :param syntax: syntax of action to show in help
        :param choices: auto completer function - possible choices generator or list of possible choices
        :return: next level subparser (with command context)
        """
        # create subparser
        subparser = SubArgsProcessor(default_action=action, parent=self)
        self._rules_commands.append(
            CommandArgRule(action=action, subparser=subparser, keywords=keywords, help=help,
                           syntax=syntax, choices=choices))
        return subparser

    def add_primary_option(self, keywords, action=None, help=None, syntax=None):
        self._rules_primary_options.append(
            PrimaryOptionRule(action=action, keywords=keywords, help=help,
                              syntax=syntax))
        return self

    def add_param(self, name=None, keywords=None, help=None, choices=None,
                  required=False):
        """
        Add parameter to retrieve later on. Syntax: '--param value' or '--param=value'
        :param name: param name
        :param keywords: trigger name or names (string or list of strings)
        :param help: description of param to show in help
        :param choices: auto completer function - possible choices generator or list of possible choices
        :param required: is param required
        :return: this parser
        """
        name = self._get_keyword_from_name(name)
        # complete keyword if not given
        if not keywords:
            keywords = name
        syntax = '<%s>' % self._trim_hyphens(name)
        self._rules_params.append(
            ParamArgRule(name=name, required=required, keywords=keywords, help=help, choices=choices,
                         syntax=syntax))
        return self

    def add_flag(self, name, keywords=None, help=None):
        """
        Add flag to check later on. Syntax: '--flag', '-f'
        :param name: flag name
        :param keywords: trigger name or names (string or list of strings)
        If missing, keywords will be autogenerated (--name or -n)
        :param help: description of flag to show in help
        :return: this parser
        """
        name = self._get_keyword_from_name(name)
        # complete keyword if not given
        if not keywords:
            keywords = name
        self._rules_flags.append(FlagArgRule(name=name, keywords=keywords, help=help))
        return self

    @staticmethod
    def _get_keyword_from_name(name):
        if name.startswith('-'):
            return name
        if len(name) == 1:
            return '-%s' % name
        else:
            return '--%s' % name

    @staticmethod
    def _trim_hyphens(strin):
        while strin.startswith('-'):
            strin = strin[1:]
        return strin

    # Getting args
    def poll_next(self, required_name=None):
        """return next arg and remove"""
        if not self.has_next():
            if required_name:
                raise CliSyntaxError('no required argument "%s" given' % required_name)
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
        # process primary options first - only one primary option
        if not self._process_primary_options():
            # then the flags and params
            self._process_flags()
            self._process_params()
            if self._args_que:
                # then commands
                self._process_commands()
            else:
                # if there's no arguments left - run default action
                self._invoke_default_action()
        # if some args left
        self._print_redundant_args()

    def _process_primary_options(self):
        self._argsOffset = 0
        while self.has_next():
            next_arg = self.peek_next()
            rule = self._find_rule_by_keyword(self._rules_primary_options, next_arg)
            if rule:
                # remove arg from list
                self.poll_next()
                # run the action
                self._invoke_action(rule.action)
                return True  # one primary option only
            else:
                # skip it - it's not what we're looking for
                self._argsOffset += 1

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
                # mark param as processed
                processed_params.append(rule)
            else:
                self._argsOffset += 1  # skip to next
        # check for unprocessed required params
        unprocessed = filter(lambda r: r.required and r not in processed_params, self._rules_params)
        unprocessed = list(map(lambda r: r.name, unprocessed))
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
        else:
            # if not recognized - run default action
            self._invoke_default_action()

    def _invoke_default_action(self):
        if self._default_action:
            # run default action without removing args
            self._invoke_action(self._default_action)
        elif self.parent:
            # no default action - try to run parent default action
            self.parent._invoke_default_action()

    def _print_redundant_args(self):
        self._argsOffset = 0
        if self.has_next():
            warn('invalid arguments: %s' % self.poll_remaining_joined(' '))

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
        name2 = self._get_keyword_from_name(name)
        val1 = self._params.get(name, None)
        if val1:
            return val1
        val2 = self._params.get(name2, None)
        if val2:
            return val2
        if required and not val1 and not val2:
            raise CliSyntaxError('no required param given: %s' % name)

    def is_param(self, name):
        return self.get_param(name) is not None

    # setting / getting flags
    def set_flag(self, name):
        if name not in self._flags:
            self._flags.append(name)

    def is_flag_set(self, name):
        name2 = self._get_keyword_from_name(name)
        return name in self._flags or name2 in self._flags

    def print_commands(self, command_rule, syntax_padding, prefix=''):
        # command help
        if self._default_action or command_rule.syntax or command_rule.help:
            print('  %s%s' % (prefix, command_rule.display_help(syntax_padding - len(prefix))))
        # and all its children
        prefix += command_rule._display_syntax_prefix() + ' '
        for subrule in self._rules_flags + self._rules_params:
            display_help_out = prefix + subrule.display_syntax()
            if subrule.help:
                display_help_out = display_help_out.ljust(syntax_padding) + ' - ' + subrule.help
            print('  %s' % display_help_out)
        # next level sub commands
        for subcommand in self._rules_commands:
            subcommand.subparser.print_commands(subcommand, syntax_padding, prefix)

    def bash_install(self):
        """
        Installs script link in /usr/bin/{appname}
        and Creates bash autocompletion script
        """
        app_name = self.poll_next('appname')
        # creating /usr/bin/ link
        usr_bin_executable = '/usr/bin/%s' % app_name
        if file_exists(usr_bin_executable):
            warn('file %s already exists - skipping.' % usr_bin_executable)
        else:
            script_path = script_real_path()
            info('creating link: %s -> %s' % (usr_bin_executable, script_path))
            shell('ln -s %s %s' % (script_path, usr_bin_executable))
        script_name = '/etc/bash_completion.d/autocomplete_%s.sh' % app_name
        app_hash = hash(app_name) % (10**8)
        function_name = '_autocomplete_%s' % app_hash  # unique across bash env
        # bash autocompletion install
        shell("""cat <<'EOF' > %s
#!/bin/bash
%s() {
    COMPREPLY=( $(%s --bash-autocomplete "${COMP_LINE}") )
}
complete -F %s %s
EOF
""" % (script_name, function_name, app_name, function_name, app_name))
        info('Autocompleter has been installed in %s. Please restart your shell.' % script_name)

    def bash_autocomplete(self):
        comp_line = self.poll_remaining_joined(joiner=' ')
        if comp_line.startswith('"') and comp_line.endswith('"'):
            comp_line = comp_line[1:-1]
        parts = comp_line.split(' ')
        args = parts[1:]
        last = args[-1] if len(args) > 0 else ''
        available = self._generate_available_completions(args)
        filtered = list(filter(lambda c: c.startswith(last), available))
        # remove '...=' prefix
        filtered = list(map(lambda c: regex_replace(c, r'(.*)=(.*)', '\\2'), filtered))
        print('\n'.join(filtered))

    def _generate_available_completions(self, args):
        if not args:
            return []
        available = []
        last = args[-1] if len(args) > 0 else ''
        previous = args[-2] if len(args) > 1 else None
        # "--param value" autocompletion
        found_params = False
        if previous:
            for rule in self._rules_params:
                for keyword in rule.keywords:
                    if previous == keyword:
                        possible_choices = rule.generate_choices(self)
                        available.extend(possible_choices)
                        found_params = True
        # "--param=value" autocompletion
        for rule in self._rules_params:
            for keyword in rule.keywords:
                if last.startswith(keyword + '='):
                    possible_choices = list(map(lambda c: keyword + '=' + c, rule.generate_choices(self)))
                    available.extend(possible_choices)
                    found_params = True
        if not found_params:
            # subcommands
            found_subcommand = False
            for idx, val in enumerate(args):
                rule = self._find_rule_by_keyword(self._rules_commands, val)
                if rule:  # if found a command
                    # append this command autcompletion (if it's last command)
                    if previous == val:
                        possible_choices = rule.generate_choices(self)
                        available.extend(possible_choices)
                    if last == val:
                        available.extend([val])
                    # append subparser autocompletions
                    subargs = args[idx:]
                    subcompletions = rule.subparser._generate_available_completions(subargs)
                    available.extend(subcompletions)
                    found_subcommand = True
                    break
            if not found_subcommand:
                # available when no completer found - flags, params, primary options
                rules = self._rules_flags + self._rules_params + self._rules_primary_options
                available.extend([keyword for rule in rules for keyword in rule.keywords])
                # all subcommands only when none was found
                rules = self._rules_commands
                available.extend([keyword for rule in rules for keyword in rule.keywords])

        return available


class ArgsProcessor(SubArgsProcessor):
    def __init__(self, app_name='Command Line Application', version='0.0.1', default_action=None, syntax=None, description=None):
        super(ArgsProcessor, self).__init__(default_action)
        self._app_name = app_name
        self._version = version
        self._syntax = syntax
        self._description = description
        # default action - help
        if not self._default_action:
            self._default_action = print_help
        # bind default options: help, version
        self.add_primary_option(['-h', '--help'], action=print_help, help='display this help and exit')
        self.add_primary_option(['-v', '--version'], action=print_version, help='print version')
        self.add_primary_option('--bash-install', syntax='<appname>', action=bash_install,
                                help='installs bash script and autocompletion')
        self.add_primary_option('--bash-autocomplete', syntax='<cmdline>', action=bash_autocomplete,
                                help='return autocompletion list')

    # auto generating help output
    def _calc_min_syntax_padding(self):
        min_syntax_padding = 0
        for rule in self._rules_flags + self._rules_params + self._rules_commands + self._rules_primary_options:
            syntax_length = rule.display_syntax_max_length()
            if syntax_length > min_syntax_padding:  # min padding = max from len(syntax)
                min_syntax_padding = syntax_length
        return min_syntax_padding

    def print_help(self):
        # auto generate help
        self.print_version()
        if self._description:
            print('\nDescription:\n  %s' % self._description)
        # print main usage
        usage_syntax = sys.argv[0]
        commands_count = sum(1 for _ in self._rules_commands)
        options_count = sum(1 for _ in self._rules_flags + self._rules_params + self._rules_primary_options)
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
            for rule in self._rules_flags + self._rules_params + self._rules_primary_options:
                print('  %s' % rule.display_help(syntax_padding))

    def print_version(self):
        print('%s v%s' % (self._app_name, self._version))


# commands available to invoke (workaround for invoking by function reference)
def print_help(ap):
    if ap.parent:
        ap = ap.parent
    ap.print_help()


def print_version(ap):
    ap.print_version()


def bash_install(ap):
    ap.bash_install()


def bash_autocomplete(ap):
    ap.bash_autocomplete()
