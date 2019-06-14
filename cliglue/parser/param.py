from typing import Optional, Any

from cliglue.args.args_que import ArgsQue
from cliglue.builder.rule import ParameterRule, ValueRule
from .error import CliSyntaxError


def match_param(rule: ParameterRule, args: ArgsQue, arg: str) -> Optional[str]:
    for keyword in rule.keywords:
        # match 2 args: --name value
        if arg == keyword:
            args.pop_current()
            if not args.has_next():
                raise CliSyntaxError('missing value argument for parameter')
            next(args)  # jump to next index with iterator
            return args.pop_current()
        # match 1 arg: --name=value
        prefix = keyword + '='
        if arg.startswith(prefix):
            return args.pop_current()[len(prefix):]
    return None


def parse_argument_value(rule: ValueRule, arg: str) -> Any:
    try:
        # custom parser
        if callable(rule.type):
            return rule.type(arg)
        # cast to custom type or default types
        return rule.type(arg)
    except ValueError as e:
        raise CliSyntaxError('conversion error') from e
