import sys
from typing import List, Set, Optional

from dataclasses import dataclass

from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, SubcommandRule, \
    PositionalArgumentRule, AllArgumentsRule
from cliglue.parser.context import RunContext
from cliglue.parser.error import CliError
from cliglue.parser.keyword import names_from_keywords
from cliglue.parser.parser import Parser
from cliglue.parser.rule_process import filter_rules


@dataclass
class _OptionHelp(object):
    cmd: str
    help: str
    parent: '_OptionHelp' = None


def print_help(rules: List[CliRule], app_name: str, version: str, help: str, subargs: List[str]):
    helps = generate_help(rules, app_name, version, help, subargs)
    print('\n'.join(helps))


def generate_help(rules: List[CliRule], app_name: str, version: str, help: str, subargs: List[str]) -> List[str]:
    available_subcommands = filter_rules(rules, SubcommandRule)
    try:
        run_context: Optional[RunContext] = Parser(rules, dry=True).parse_args(subargs)
        all_rules: List[CliRule] = run_context.active_rules
        active_subcommands: List[SubcommandRule] = run_context.active_subcommands
        precommands: List[str] = [_subcommand_short_name(rule) for rule in active_subcommands]
        if active_subcommands:
            available_subcommands = filter_rules(active_subcommands[-1].subrules, SubcommandRule)
    except CliError:
        all_rules: List[CliRule] = rules
        precommands: List[str] = []

    return generate_subcommand_help(all_rules, app_name, version, help, precommands, available_subcommands)


def generate_subcommand_help(
        all_rules: List[CliRule],
        app_name: str,
        version: str,
        help: str,
        precommands: List[str],
        subcommands: List[SubcommandRule],
) -> List[str]:
    flags = filter_rules(all_rules, FlagRule)
    parameters = filter_rules(all_rules, ParameterRule)
    primary_options = filter_rules(all_rules, PrimaryOptionRule)
    pos_arguments = filter_rules(all_rules, PositionalArgumentRule)
    all_args = filter_rules(all_rules, AllArgumentsRule)

    options: List[_OptionHelp] = _generate_options_helps(all_rules)
    commands: List[_OptionHelp] = _generate_commands_helps(subcommands)

    out = []
    # App info
    app_info = app_help_info(app_name, help, version)
    if app_info:
        out.append(app_info + '\n')

    # Usage
    app_bin_prefix = ' '.join([sys.argv[0]] + precommands)
    usage_syntax: str = app_bin_prefix

    if commands:
        usage_syntax += ' [COMMAND]'

    if flags or parameters or primary_options:
        usage_syntax += ' [OPTIONS]'

    usage_syntax += usage_positional_arguments(pos_arguments)
    usage_syntax += usage_all_arguments(all_args)

    out.append(f'Usage:\n  {usage_syntax}')

    if options:
        out.append('\nOptions:')
        __helpers_output(options, out)

    if commands:
        out.append('\nCommands:')
        __helpers_output(commands, out)
        out.append(f'\nRun "{app_bin_prefix} COMMAND --help" for more information on a command.')

    return out


def app_help_info(app_name: str, help: str, version: str) -> Optional[str]:
    info = app_name_version(app_name, version)
    if help:
        if info:
            info += ' - '
        info += help
    return info


def app_name_version(app_name, version):
    info = ''
    if app_name:
        info += app_name
    if version:
        version = _normalized_version(version)
        if info:
            info += ' '
        info += version
    return info


def __helpers_output(commands, out):
    padding = _max_name_width(commands)
    for helper in commands:
        name_padded = helper.cmd.ljust(padding)
        if helper.help:
            out.append(f'  {name_padded} - {helper.help}')
        else:
            out.append(f'  {name_padded}')


def print_version(app_name: str, version: str):
    print(app_name_version(app_name, version))


def _normalized_version(version: str) -> str:
    if version.startswith('v'):
        return version
    return f'v{version}'


def _max_name_width(helps: List[_OptionHelp]) -> int:
    return max(map(lambda h: len(h.cmd), helps))


def _generate_options_helps(rules: List[CliRule]) -> List[_OptionHelp]:
    # filter non-empty
    return list(filter(lambda o: o, [_generate_option_help(rule) for rule in rules]))


def _generate_option_help(rule: CliRule) -> Optional[_OptionHelp]:
    if isinstance(rule, PrimaryOptionRule):
        return _primary_option_help(rule)
    elif isinstance(rule, FlagRule):
        return _flag_help(rule)
    elif isinstance(rule, ParameterRule):
        return _parameter_help(rule)


def _generate_commands_helps(rules: List[CliRule], parent: _OptionHelp = None) -> List[_OptionHelp]:
    commands: List[_OptionHelp] = []
    for rule in rules:
        if isinstance(rule, SubcommandRule):
            helper = _subcommand_help(rule, parent)
            commands.append(helper)
            commands.extend(_generate_commands_helps(rule.subrules, helper))
    return commands


def _subcommand_help(rule: SubcommandRule, parent: _OptionHelp) -> _OptionHelp:
    cmd = _subcommand_prefix(parent) + '|'.join(sorted_keywords(rule.keywords))
    pos_args = filter_rules(rule.subrules, PositionalArgumentRule)
    all_args = filter_rules(rule.subrules, AllArgumentsRule)
    cmd += usage_positional_arguments(pos_args)
    cmd += usage_all_arguments(all_args)
    return _OptionHelp(cmd, rule.help, parent)


def _subcommand_prefix(helper: _OptionHelp) -> str:
    if not helper:
        return ''
    return helper.cmd + ' '


def _primary_option_help(rule: PrimaryOptionRule) -> _OptionHelp:
    cmd = ', '.join(sorted_keywords(rule.keywords))
    pos_args = filter_rules(rule.subrules, PositionalArgumentRule)
    all_args = filter_rules(rule.subrules, AllArgumentsRule)
    cmd += usage_positional_arguments(pos_args)
    cmd += usage_all_arguments(all_args)
    return _OptionHelp(cmd, rule.help)


def _flag_help(rule: FlagRule) -> _OptionHelp:
    cmd = ', '.join(sorted_keywords(rule.keywords))
    return _OptionHelp(cmd, rule.help)


def _parameter_help(rule: ParameterRule) -> _OptionHelp:
    cmd = ', '.join(sorted_keywords(rule.keywords)) + ' ' + _param_var_name(rule)
    return _OptionHelp(cmd, rule.help)


def _param_var_name(rule: ParameterRule) -> str:
    if rule.name:
        return rule.name.upper()
    else:
        # get name from longest keyword
        names: Set[str] = names_from_keywords(rule.keywords)
        return max(names, key=lambda n: len(n)).upper()


def _argument_var_name(rule: PositionalArgumentRule) -> str:
    return rule.name.upper()


def _subcommand_short_name(rule: SubcommandRule) -> str:
    return next(iter(rule.keywords))


def sorted_keywords(keywords: Set[str]) -> List[str]:
    # shortest keywords first, then alphabetically
    return sorted(keywords, key=lambda k: (len(k), k))


def display_positional_argument(rule: PositionalArgumentRule) -> str:
    var_name = _argument_var_name(rule)
    if rule.required:
        return f' {var_name}'
    else:
        return f' [{var_name}]'


def display_all_arguments(rule: AllArgumentsRule) -> str:
    arg_name = rule.name.upper()
    return f' [{arg_name}...]'


def usage_positional_arguments(rules: List[PositionalArgumentRule]) -> str:
    return ''.join([display_positional_argument(rule) for rule in rules])


def usage_all_arguments(rules: List[AllArgumentsRule]) -> str:
    return ''.join([display_all_arguments(rule) for rule in rules])
