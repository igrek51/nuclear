from typing import Optional, Iterable

from cliglue.args.args_que import ArgsQue
from cliglue.builder.rule import ParameterRule
from cliglue.parser.keyword import names_from_keywords
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


def parameter_display_name(rule: ParameterRule) -> str:
    if rule.name:
        return rule.name
    else:
        return ', '.join(rule.keywords)


def parameter_var_names(rule: ParameterRule) -> Iterable[str]:
    if rule.name:
        return [rule.name]
    else:
        return names_from_keywords(rule.keywords)
