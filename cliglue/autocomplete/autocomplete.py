import inspect
import os
import re
from typing import List, Optional, Any

from cliglue.builder.rule import ValueRule
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
        warn('file %s already exists - skipping.' % usr_bin_executable)
    else:
        script_path: str = script_real_path()
        info('creating link: {} -> {}'.format(usr_bin_executable, script_path))
        shell('ln -s {} {}'.format(script_path, usr_bin_executable))
    script_name: str = '/etc/bash_completion.d/autocomplete_%s.sh' % app_name
    app_hash: int = hash(app_name) % (10 ** 8)
    function_name: str = '_autocomplete_%s' % app_hash  # should be unique across bash env
    # bash autocompletion install
    shell("""cat <<'EOF' > {}
#!/bin/bash
{}() {
COMPREPLY=( $({} --bash-autocomplete "${{COMP_LINE}}") )
}
complete -F {} {}
EOF
""".format(script_name, function_name, app_name, function_name, app_name))
    info('Autocompleter has been installed in %s. Please restart your shell.' % script_name)


def bash_autocomplete(cmdline: str):
    # extract quotes
    if cmdline.startswith('"') and cmdline.endswith('"'):
        cmdline = cmdline[1:-1]
    parts: List[str] = cmdline.split(' ')
    args: List[str] = parts[1:]
    last: str = args[-1] if len(args) > 0 else ''
    available: List[str] = _generate_available_completions(args)
    # '...=' prefix removing matcher
    re_matcher = re.compile(r'(.*)=(.*)')
    filtered: List[str] = [re_matcher.sub('\\2', c)
                           for c in available
                           if c.startswith(last)
                           ]
    print('\n'.join(filtered))


def _generate_available_completions(args: List[str]) -> List[str]:
    if not args:
        return []
    available: List[str] = []
    last: str = args[-1] if len(args) > 0 else ''
    previous: Optional[str] = args[-2] if len(args) > 1 else None
    # "--param value" autocompletion
    found_params: bool = False

    if previous:
        for rule in self._rules_params:
            for keyword in rule.keywords:
                if previous == keyword:
                    possible_choices: List[str] = generate_choices(rule)
                    available.extend(possible_choices)
                    found_params = True

    # "--param=value" autocompletion
    for rule in self._rules_params:
        for keyword in rule.keywords:
            if last.startswith(keyword + '='):
                possible_choices: List[str] = list(map(lambda c: keyword + '=' + c, generate_choices(rule)))
                available.extend(possible_choices)
                found_params = True

    if not found_params:
        # subcommands
        found_subcommand = False
        for idx, val in enumerate(args):
            rule: CommandArgRule = self._find_rule_by_keyword(self._rules_commands, val)
            if rule:  # if found a command
                # append this command autcompletion (if it's last command)
                if previous == val:
                    possible_choices: List[str] = generate_choices(rule)
                    available.extend(possible_choices)
                if last == val:
                    available.extend([val])
                # append subparser autocompletions
                subargs: List[str] = args[idx:]
                subcompletions: List[str] = rule.subparser._generate_available_completions(subargs)
                available.extend(subcompletions)
                found_subcommand = True
                break
        if not found_subcommand:
            # available when no completer found - flags, params, primary options
            rules: List[CliArgRule] = self._rules_flags + self._rules_params + self._rules_primary_options
            available.extend([keyword for rule in rules for keyword in rule.keywords])
            # all subcommands only when none was found
            rules = self._rules_commands
            available.extend([keyword for rule in rules for keyword in rule.keywords])

    return available


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