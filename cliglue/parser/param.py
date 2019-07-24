from typing import Optional, Iterable

from cliglue.args.args_que import ArgsQue
from cliglue.builder.rule import ParameterRule
from cliglue.parser.keyword import format_var_names
from .error import CliSyntaxError


def match_param(rule: ParameterRule, args: ArgsQue, arg: str) -> Optional[str]:
    for keyword in rule.keywords:
        # match 2 args: --name value
        if arg == keyword:
            args.pop_current()
            if not args.has_next():
                raise CliSyntaxError('missing value argument for parameter')
            return args.pop_current()
        # match 1 arg: --name=value
        prefix = keyword + '='
        if arg.startswith(prefix):
            return args.pop_current()[len(prefix):]
    return None


def parameter_default_value(rule: ParameterRule):
    if rule.multiple:
        if not rule.default:
            return []
        elif not isinstance(rule.default, list):
            return [rule.default]
        else:
            return rule.default
    else:
        return rule.default
