import sys
from typing import List

from cliglue.parser.keyword import name_from_keyword
from cliglue.builder.rule import PrimaryOptionRule, ParameterRule, FlagRule, CliRule, SubcommandRule, filter_rules


def print_help(rules: List[CliRule],
               app_name: str = None,
               version: str = None,
               help: str = None
               ):
    print_version(app_name, version)

    if help:
        print('\nDescription:\n  {}'.format(help))

    usage_syntax: str = sys.argv[0]

    commands = filter_rules(rules, SubcommandRule)
    flags = filter_rules(rules, FlagRule)
    parameters = filter_rules(rules, ParameterRule)
    primary_options = filter_rules(rules, PrimaryOptionRule)

    for rule in primary_options:
        for keyword in rule.keywords:
            usage_syntax += ' [{}]'.format(keyword)
    for rule in flags:
        for keyword in rule.keywords:
            usage_syntax += ' [{}]'.format(keyword)

    for rule in parameters:
        for keyword in rule.keywords:
            name = name_from_keyword(keyword).upper()
            if rule.required:
                usage_syntax += ' {} {}'.format(keyword, name)
            else:
                usage_syntax += ' [{} {}]'.format(keyword, name)

    if commands:
        usage_syntax += ' <command>'

    print('\nUsage:\n  %s' % usage_syntax)

    if commands:
        print('\nCommands:')
        for rule in commands:
            _print_help_command(rule)

    # options
    if primary_options or flags or parameters:
        print('\nOptions:')
        for rule in primary_options:
            _print_help_primary_option(rule)
        for rule in flags:
            _print_help_flag(rule)
        for rule in parameters:
            _print_help_parameter(rule)

    # TODO multilevel subhelps for subcommands


def print_version(app_name: str = None,
                  version: str = None):
    if not version.startswith('v'):
        version = 'v{}'.format(version)
    print('{} v{}'.format(app_name, version))


def _print_help_command(rule: SubcommandRule, prefix: str = ''):
    prefix += ', '.join(rule.keywords)
    print('  {}'.format(prefix))
    if rule.help:
        print('    {}'.format(rule.help))
    # deeper subcommands
    prefix += ' '
    for subrule in rule.subrules:
        _print_help_command(subrule, prefix)


def _print_help_primary_option(rule: PrimaryOptionRule):
    print('  {}'.format(', '.join(rule.keywords)))
    if rule.help:
        print('    {}'.format(rule.help))


def _print_help_flag(rule: FlagRule):
    print('  {}'.format(', '.join(rule.keywords)))
    if rule.help:
        print('    {}'.format(rule.help))


def _print_help_parameter(rule: ParameterRule):
    name = name_from_keyword(next(iter(rule.keywords))).upper()
    print('  {} {}'.format(', '.join(rule.keywords), name))
    if rule.help:
        print('    {}'.format(rule.help))
