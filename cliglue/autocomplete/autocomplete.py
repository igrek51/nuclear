import re
import shlex
from typing import List, Optional

from cliglue.builder.rule import CliRule, ParameterRule, FlagRule, SubcommandRule, PrimaryOptionRule, \
    PositionalArgumentRule, ManyArgumentsRule
from cliglue.parser.context import RunContext
from cliglue.parser.error import CliError
from cliglue.parser.parser import Parser
from cliglue.parser.transform import filter_rules
from cliglue.parser.value import generate_value_choices


# TODO not only the last argument may be focused on
def bash_autocomplete(rules: List[CliRule], cmdline: str):
    filtered = find_matching_completions(cmdline, rules)
    print('\n'.join(filtered))


def find_matching_completions(cmdline, rules) -> List[str]:
    extracted_cmdline = _extract_quotes(cmdline)
    args: List[str] = extract_args(extracted_cmdline)
    current_word: str = args[-1] if len(args) > 0 else ''
    available: List[str] = _find_available_completions(rules, args, current_word)
    # convert '--param=value' proposals to 'value'
    hyphen_param_matcher = re.compile(r'-(.+)=(.+)')
    return [
        hyphen_param_matcher.sub('\\2', c)
        for c in available
        if c.startswith(current_word)
    ]


def extract_args(extracted_cmdline):
    args = shlex.split(extracted_cmdline)[1:]
    # restore last whitespace
    if extracted_cmdline.endswith(' ') or extracted_cmdline.endswith('\t'):
        args.append('')
    return args


def _extract_quotes(cmdline):
    if cmdline.startswith('"') and cmdline.endswith('"'):
        return cmdline[1:-1]
    return cmdline


def _find_available_completions(rules: List[CliRule], args: List[str], current_word: str) -> List[str]:
    subcommands: List[SubcommandRule] = filter_rules(rules, SubcommandRule)
    run_context: Optional[RunContext] = Parser(rules, dry=True).parse_args(args)
    all_rules: List[CliRule] = run_context.active_rules
    active_subcommands: List[SubcommandRule] = run_context.active_subcommands
    if active_subcommands:
        subcommands = filter_rules(active_subcommands[-1].subrules, SubcommandRule)

        # current word is exactly the last command
        if current_word in active_subcommands[-1].keywords:
            return [current_word]

    flags = filter_rules(all_rules, FlagRule)
    parameters = filter_rules(all_rules, ParameterRule)
    primary_options = filter_rules(all_rules, PrimaryOptionRule)
    pos_arguments = filter_rules(all_rules, PositionalArgumentRule)
    many_args = filter_rules(all_rules, ManyArgumentsRule)

    # "--param value" autocompletion
    previous: Optional[str] = args[-2] if len(args) > 1 else None
    if previous:
        for rule in parameters:
            for keyword in rule.keywords:
                if previous == keyword:
                    possible_choices: List[str] = generate_value_choices(rule)
                    return possible_choices

    # "--param=value" autocompletion
    for rule in parameters:
        for keyword in rule.keywords:
            if current_word.startswith(keyword + '='):
                possible_choices: List[str] = list(map(lambda c: keyword + '=' + c, generate_value_choices(rule)))
                return possible_choices

    completions: List[str] = []
    # subcommands
    for rule in subcommands:
        completions.extend(rule.keywords)

    # flags, parameter names, primary options
    for rule in flags:
        completions.extend(rule.keywords)

    for rule in parameters:
        for keyword in rule.keywords:
            completions.append(keyword)
            completions.append(keyword + '=')

    for rule in primary_options:
        completions.extend(rule.keywords)

    # positional arguments
    for rule in pos_arguments:
        possible_choices: List[str] = generate_value_choices(rule)
        completions.extend(possible_choices)
    for rule in many_args:
        possible_choices: List[str] = generate_value_choices(rule)
        completions.extend(possible_choices)

    return completions
