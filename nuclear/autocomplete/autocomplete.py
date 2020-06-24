import re
import shlex
from typing import List, Optional

from nuclear.builder.rule import CliRule, ParameterRule, FlagRule, SubcommandRule, PrimaryOptionRule, \
    PositionalArgumentRule, ManyArgumentsRule
from nuclear.parser.context import RunContext
from nuclear.parser.parser import Parser
from nuclear.parser.transform import filter_rules
from nuclear.parser.value import generate_value_choices


def bash_autocomplete(rules: List[CliRule], cmdline: str, word_idx: Optional[int]):
    filtered = find_matching_completions(cmdline, rules, word_idx)
    print('\n'.join(filtered))


def find_matching_completions(cmdline, rules, word_idx: Optional[int]) -> List[str]:
    extracted_cmdline = _extract_quotes(cmdline)
    try:
        args: List[str] = extract_args(extracted_cmdline)
    except ValueError:
        return []
    current_word: str = get_current_word(args, word_idx)
    available: List[str] = _find_available_completions(rules, args, current_word)
    # convert '--param=value' proposals to 'value'
    hyphen_param_matcher = re.compile(r'-(.+)=(.+)')
    return [
        escape_spaces(hyphen_param_matcher.sub('\\2', c))
        for c in available
        if c.startswith(current_word)
    ]


def escape_spaces(name: str) -> str:
    return name.replace(' ', '\\ ')


def extract_args(extracted_cmdline) -> List[str]:
    args = shlex.split(extracted_cmdline)[1:]
    # restore last whitespace
    if extracted_cmdline.endswith(' ') or extracted_cmdline.endswith('\t'):
        args.append('')
    return args


def _extract_quotes(cmdline) -> str:
    if cmdline.startswith('"') and cmdline.endswith('"'):
        return cmdline[1:-1]
    return cmdline


def get_current_word(args: List[str], word_idx: Optional[int]) -> str:
    if word_idx is None or word_idx - 1 >= len(args):
        return args[-1] if len(args) > 0 else ''
    return args[word_idx - 1]


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
                    possible_choices: List[str] = generate_value_choices(rule, current=current_word)
                    return possible_choices

    # "--param=value" autocompletion
    for rule in parameters:
        for keyword in rule.keywords:
            if current_word.startswith(keyword + '='):
                possible_choices: List[str] = list(map(lambda c: keyword + '=' + c,
                                                       generate_value_choices(rule, current=current_word)))
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
        possible_choices: List[str] = generate_value_choices(rule, current=current_word)
        completions.extend(possible_choices)
    for rule in many_args:
        possible_choices: List[str] = generate_value_choices(rule, current=current_word)
        completions.extend(possible_choices)

    return completions
