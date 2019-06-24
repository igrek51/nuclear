import inspect
import os
import re
import shlex
from typing import List, Optional, Any

from cliglue.builder.rule import ValueRule, CliRule, ParameterRule, FlagRule, SubcommandRule, PrimaryOptionRule, \
    PositionalArgumentRule, AllArgumentsRule, KeywordRule
from cliglue.parser.rule_process import filter_rules
from cliglue.utils.files import script_real_path
from cliglue.utils.output import warn, info
from cliglue.utils.shell import shell


def bash_install(app_name: str):
    """
    Installs script link in /usr/bin/{app_name}
    and Creates bash autocompletion script
    """
    # creating /usr/bin/ link
    usr_bin_executable: str = '/usr/bin/%s' % app_name
    if os.path.isfile(usr_bin_executable):
        warn(f'file {usr_bin_executable} already exists - skipping.')
    else:
        script_path: str = script_real_path()
        info(f'creating link: {usr_bin_executable} -> {script_path}')
        shell(f'ln -s {script_path} {usr_bin_executable}')
    script_name: str = '/etc/bash_completion.d/autocomplete_%s.sh' % app_name
    app_hash: int = hash(app_name) % (10 ** 8)
    function_name: str = '_autocomplete_%s' % app_hash  # should be unique across bash env
    # bash autocompletion install
    shell(f"""cat <<'EOF' > {script_name}
#!/bin/bash
{function_name}() {{
COMPREPLY=( $({app_name} --bash-autocomplete ${{COMP_LINE}}) )
}}
complete -F {function_name} {app_name}
EOF
""")
    info(f'Autocompleter has been installed in {script_name}. Please restart your shell.')


def bash_autocomplete(rules: List[CliRule], cmdline: str):
    filtered = find_matching_completions(cmdline, rules)
    print('\n'.join(filtered))


def find_matching_completions(cmdline, rules) -> List[str]:
    args: List[str] = shlex.split(cmdline)[1:]
    current_word: str = args[-1] if len(args) > 0 else ''
    available: List[str] = _find_available_completions(rules, args, current_word)
    # convert '--param=value' proposals to 'value'
    hyphen_param_matcher = re.compile(r'(.*)=(.*)')
    return [
        hyphen_param_matcher.sub('\\2', c)
        for c in available
        if c.startswith(current_word)
    ]


def _extract_quotes(cmdline):
    if cmdline.startswith('"') and cmdline.endswith('"'):
        return cmdline[1:-1]
    return cmdline


def _find_available_completions(rules: List[CliRule], args: List[str], current_word: str) -> List[str]:
    return _find_available_subcompletions(rules, args, current_word, [])


def _find_available_subcompletions(rules: List[CliRule], args: List[str], current_word: str, completions: List[str]) -> List[str]:
    if not args:
        return []

    command_rules = filter_rules(rules, SubcommandRule)
    flags = filter_rules(rules, FlagRule)
    parameters = filter_rules(rules, ParameterRule)
    primary_options = filter_rules(rules, PrimaryOptionRule)
    pos_arguments = filter_rules(rules, PositionalArgumentRule)
    all_args = filter_rules(rules, AllArgumentsRule)

    # # "--param value" autocompletion
    # found_params: bool = False
    # previous: Optional[str] = args[-2] if len(args) > 1 else None
    # if previous:
    #     for rule in parameters:
    #         for keyword in rule.keywords:
    #             if previous == keyword:
    #                 possible_choices: List[str] = generate_choices(rule)
    #                 completions.extend(possible_choices)
    #                 found_params = True
    #
    # # "--param=value" autocompletion
    # for rule in parameters:
    #     for keyword in rule.keywords:
    #         if current_word.startswith(keyword + '='):
    #             possible_choices: List[str] = list(map(lambda c: keyword + '=' + c, generate_choices(rule)))
    #             completions.extend(possible_choices)
    #             found_params = True
    #
    # if not found_params:
    #     # subcommands
    #     found_subcommand = False
    #     for idx, val in enumerate(args):
    #     for rule in command_rules:
    #         if first in rule.keywords:
    #             # append this command autcompletion (if it's last command)
    #             if previous == val:
    #                 possible_choices: List[str] = generate_choices(rule)
    #                 completions.extend(possible_choices)
    #             if current_word == val:
    #                 completions.extend([val])
    #             # append subparser autocompletions
    #             subargs: List[str] = args[idx:]
    #             subcompletions: List[str] = rule.subparser._generate_available_completions(subargs)
    #             completions.extend(subcompletions)
    #             found_subcommand = True
    #             break
    #     if not found_subcommand:
    #         # available when no completer found - flags, parameter names, primary options
    #         rules: List[KeywordRule] = filter_rules(rules, KeywordRule)
    #         completions.extend([keyword for rule in rules for keyword in rule.keywords])
    #         # all subcommands only when none was found
    #         rules = self._rules_commands
    #         completions.extend([keyword for rule in rules for keyword in rule.keywords])

    return completions


def generate_choices(rule: ValueRule) -> List[Any]:
    if not rule.choices:
        return []
    elif isinstance(rule.choices, list):
        return rule.choices
    else:
        (args, _, _, _, _, _, _) = inspect.getfullargspec(rule.choices)
        if args:
            # TODO generate choices based on the current arguments
            return []
        else:
            return rule.choices()
