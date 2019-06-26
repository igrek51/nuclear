import sys
from typing import Any, List, Optional

from cliglue.autocomplete.autocomplete import bash_install, bash_autocomplete
from cliglue.help.help import print_version, print_help
from cliglue.parser.error import CliError, CliSyntaxError, CliDefinitionError
from cliglue.parser.parser import Parser
from cliglue.utils.output import error
from .rule import SubcommandRule, PrimaryOptionRule, ParameterRule, PositionalArgumentRule, AllArgumentsRule, \
    DefaultActionRule, FlagRule, CliRule
from .typedef import Action, ChoiceProvider, TypeOrParser


def subcommand(
        *keywords: str,
        run: Action = None,
        help: str = None,
) -> SubcommandRule:
    return SubcommandRule(help, set(keywords), run)


def flag(
        *keywords: str,
        help: str = None,
) -> FlagRule:
    return FlagRule(set(keywords), help)


def parameter(
        *keywords: str,
        name: str = None,
        help: str = None,
        required: bool = False,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
) -> ParameterRule:
    return ParameterRule(set(keywords), name, required, default, type, choices, help)


def primary_option(
        *keywords: str,
        run: Action = None,
        help: str = None,
) -> PrimaryOptionRule:
    return PrimaryOptionRule(help, set(keywords), run)


def argument(
        name: str,
        help: str = None,
        required: bool = True,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
) -> PositionalArgumentRule:
    return PositionalArgumentRule(name, required, default, type, choices, help)


def all_arguments(
        name: str,
        joined_with: Optional[str] = None,
) -> AllArgumentsRule:
    return AllArgumentsRule(name, joined_with)


def default_action(
        run: Action = None,
) -> DefaultActionRule:
    return DefaultActionRule(run)


class CliBuilder(object):
    def __init__(self,
                 name: str = None,
                 version: str = None,
                 help: str = None,
                 run: Action = None,
                 with_defaults: bool = True,
                 help_onerror: bool = True,
                 reraise_error: bool = False,
                 ):
        self.__name: str = name
        self.__version: str = version
        self.__help: str = help
        self.__subrules: List[CliRule] = []

        if run:
            self.has(default_action(run))

        self.__help_onerror: bool = help_onerror
        self.__reraise_error: bool = reraise_error
        if with_defaults:
            self.__add_default_rules()

    def has(self, *subrules: CliRule) -> 'CliBuilder':
        self.__subrules += subrules
        return self

    def run(self):
        self.run_with_args(sys.argv[1:])

    def run_with_args(self, args: List[str]):
        try:
            Parser(self.__subrules).parse_args(args)
        except CliDefinitionError as e:
            error(f'CLI Definition error: {e}')
            raise e
        except CliSyntaxError as e:
            error(f'Syntax error: {e}')
            if self.__help_onerror:
                self.print_help([])
            if self.__reraise_error:
                raise e

    def print_help(self, sucommands: List[str]):
        print_help(self.__subrules, self.__name, self.__version, self.__help, sucommands)

    def bash_autocomplete(self, cmdline: str):
        bash_autocomplete(self.__subrules, cmdline)

    def __add_default_rules(self):
        def __print_root_help():
            self.print_help([])

        def __print_subcommand_help(sucommands: List[str]):
            self.print_help(sucommands)

        def __print_version():
            print_version(self.__name, self.__version)

        def __bash_install(app_name: str):
            bash_install(app_name)

        def __bash_autocomplete(cmdline: str):
            self.bash_autocomplete(cmdline)

        self.has(
            primary_option('-h', '--help', run=__print_subcommand_help, help='Display this help and exit').has(
                all_arguments('sucommands'),
            ),
            primary_option('--version', run=__print_version, help='Print version information and exit'),
            primary_option('--bash-install', run=__bash_install,
                           help='Install script as a bash binary and add autocompletion links').has(
                argument('app-name', help='binary name'),
            ),
            primary_option('--bash-autocomplete', run=__bash_autocomplete,
                           help='Return matching autocompletion proposals').has(
                all_arguments('cmdline', joined_with=' '),
            ),
        )

        if not self.__has_default_action():
            self.has(default_action(__print_root_help))

    def __has_default_action(self) -> bool:
        return any([isinstance(rule, DefaultActionRule) for rule in self.__subrules])
