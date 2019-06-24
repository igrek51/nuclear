from typing import Optional, List

from dataclasses import dataclass

from cliglue.args.container import ArgsContainer
from cliglue.builder.rule import SubcommandRule, CliRule
from cliglue.builder.typedef import Action


@dataclass
class RunContext(object):
    args_container: ArgsContainer
    action: Optional[Action]
    active_subcommands: List[SubcommandRule]
    active_rules: List[CliRule]
