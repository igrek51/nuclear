import sys
from typing import List, Set

from dataclasses import dataclass

from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, SubcommandRule, filter_rules, \
    PositionalArgumentRule, AllArgumentsRule
from cliglue.parser.keyword import names_from_keywords


@dataclass
class _OptionHelp(object):
    cmd: str
    help: str
    parent: '_OptionHelp' = None


def print_help(rules: List[CliRule], app_name: str, version: str, help: str, subcommands: List[str]):
    # App info
    app_info: str = app_name
    if version:
        version = _normalized_version(version)
        app_info += f' {version}'
    if help:
        app_info += f' - {help}'
    print(app_info)

    # Usage
    app_bin = sys.argv[0]
    usage_syntax: str = app_bin

    command_rules = filter_rules(rules, SubcommandRule)
    flags = filter_rules(rules, FlagRule)
    parameters = filter_rules(rules, ParameterRule)
    primary_options = filter_rules(rules, PrimaryOptionRule)
    pos_arguments = filter_rules(rules, PositionalArgumentRule)
    all_args = filter_rules(rules, AllArgumentsRule)

    for rule in flags:
        for keyword in rule.keywords:
            usage_syntax += f' [{keyword}]'

    for rule in parameters:
        keywords_joined = '|'.join(rule.keywords)
        var_name = _param_var_name(rule)
        if rule.required:
            usage_syntax += f' {keywords_joined} {var_name}'
        else:
            usage_syntax += f' [{keywords_joined} {var_name}]'

    for rule in primary_options:
        for keyword in rule.keywords:
            usage_syntax += f' [{keyword}]'

    if command_rules:
        usage_syntax += ' COMMAND'

    for rule in pos_arguments:
        var_name = _argument_var_name(rule)
        if rule.required:
            usage_syntax += f' {var_name}'
        else:
            usage_syntax += f' [{var_name}]'

    for rule in all_args:
        usage_syntax += f' [{rule.name}...]'

    print(f'\nUsage:\n  {usage_syntax}')

    # commands & options
    options: List[_OptionHelp] = []
    _add_options_helps(options, rules)
    commands: List[_OptionHelp] = []
    _add_commands_helps(commands, command_rules)

    if options:
        print('\nOptions:')
        padding = _max_name_width(options)
        for helper in options:
            name_padded = helper.cmd.ljust(padding)
            if helper.help:
                print(f'  {name_padded} - {helper.help}')
            else:
                print(f'  {name_padded}')

    if commands:
        print('\nCommands:')
        padding = _max_name_width(commands)
        for helper in commands:
            name_padded = helper.cmd.ljust(padding)
            if helper.help:
                print(f'  {name_padded} - {helper.help}')
            else:
                print(f'  {name_padded}')

        print(f'\nRun "{app_bin} COMMAND --help" for more information on a command.')

    sys.exit(0)


def print_version(app_name: str, version: str):
    if version:
        version = _normalized_version(version)
        print(f'{app_name} {version}')
    else:
        print(app_name)


def _normalized_version(version: str) -> str:
    if version.startswith('v'):
        return version
    return f'v{version}'


def _max_name_width(helps: List[_OptionHelp]) -> int:
    return max(map(lambda h: len(h.cmd), helps))


def _add_options_helps(options: List[_OptionHelp], rules: List[CliRule]):
    for rule in rules:
        if isinstance(rule, PrimaryOptionRule):
            options.append(_primary_option_help(rule))
        elif isinstance(rule, FlagRule):
            options.append(_flag_help(rule))
        elif isinstance(rule, ParameterRule):
            options.append(_parameter_help(rule))


def _add_commands_helps(commands: List[_OptionHelp], rules: List[CliRule], parent: _OptionHelp = None):
    for rule in rules:
        if isinstance(rule, SubcommandRule):
            helper = _subcommand_help(rule, parent)
            commands.append(helper)
            _add_commands_helps(commands, rule.subrules, helper)


def _subcommand_prefix(helper: _OptionHelp) -> str:
    if not helper:
        return ''
    return helper.cmd + ' '


def _subcommand_help(rule: SubcommandRule, parent: _OptionHelp) -> _OptionHelp:
    cmd = _subcommand_prefix(parent) + '|'.join(rule.keywords)
    return _OptionHelp(cmd, rule.help, parent)


def _primary_option_help(rule: PrimaryOptionRule) -> _OptionHelp:
    cmd = ', '.join(rule.keywords)
    return _OptionHelp(cmd, rule.help)


def _flag_help(rule: FlagRule) -> _OptionHelp:
    cmd = ', '.join(rule.keywords)
    return _OptionHelp(cmd, rule.help)


def _parameter_help(rule: ParameterRule) -> _OptionHelp:
    cmd = ', '.join(rule.keywords) + ' ' + _param_var_name(rule)
    return _OptionHelp(cmd, rule.help)


def _param_var_name(rule: ParameterRule) -> str:
    if rule.name:
        return rule.name.upper()
    else:
        # get name from longest keyword
        names: Set[str] = names_from_keywords(rule.keywords)
        return max(names, lambda n: len(n)).upper()


def _subcommand_short_name(rule: SubcommandRule) -> str:
    return rule.keywords[0]


def _argument_var_name(rule: PositionalArgumentRule) -> str:
    return rule.name.upper()
