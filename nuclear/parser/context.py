from dataclasses import dataclass
from typing import Optional, List, Any, Dict

from nuclear.args.container import ArgsContainer
from nuclear.builder.rule import SubcommandRule, CliRule
from nuclear.builder.typedef import Action


@dataclass
class RunContext(object):
    args_container: ArgsContainer
    action: Optional[Action]
    active_subcommands: List[SubcommandRule]
    active_rules: List[CliRule]
    internal_vars: Dict[str, Any]
