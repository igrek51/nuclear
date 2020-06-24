from typing import Optional, Tuple

from nuclear.args.args_que import ArgsQue
from nuclear.builder.rule import DictionaryRule
from nuclear.builder.rule import ParameterRule
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


def match_dictionary(rule: DictionaryRule, args: ArgsQue, arg: str
                     ) -> Tuple[Optional[str], Optional[str]]:
    for keyword in rule.keywords:
        # match 3 args: --keyword name value
        if arg == keyword:
            args.pop_current()
            if not args.has_next():
                raise CliSyntaxError('missing key argument for dictionary')
            var_key = args.pop_current()
            if not args.has_next():
                raise CliSyntaxError('missing value argument for dictionary')
            var_value = args.pop_current()
            return var_key, var_value
    return None, None
