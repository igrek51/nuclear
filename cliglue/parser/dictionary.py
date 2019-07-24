from typing import Optional, Tuple, Iterable

from cliglue.args.args_que import ArgsQue
from cliglue.builder.rule import DictionaryRule
from cliglue.parser.keyword import format_var_names
from .error import CliSyntaxError


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
