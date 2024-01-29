from dataclasses import dataclass
from typing import Optional, List, Any, Dict

from nuclear.cli.args.container import ArgsContainer
from nuclear.cli.builder.rule import SubcommandRule, CliRule
from nuclear.cli.builder.typedef import Action


@dataclass
class RunContext:
    args_container: ArgsContainer
    action: Optional[Action]
    active_subcommands: List[SubcommandRule]
    active_rules: List[CliRule]
    internal_vars: Dict[str, Any]
