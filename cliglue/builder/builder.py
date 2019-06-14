import sys
from typing import Any, List, Optional

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
                 ):
        self.__name: str = name
        self.__version: str = version
        self.__help: str = help
        self.__subrules: List[CliRule] = []
        self.__run: Action = run
        self.__help_onerror: bool = help_onerror
        if with_defaults:
            self.__add_default_rules()

    def has(self, *subrules: CliRule) -> 'CliBuilder':
        self.__subrules += subrules
        return self

    def run(self):
        self.run_with_args(sys.argv[1:])

    def run_with_args(self, args: List[str]):
        try:
            Parser(self.__subrules, self.__run).parse_args(args)
        except CliDefinitionError as e:
            error(e)
            raise e
        except CliSyntaxError as e:
            error(e)
            if self.__help_onerror:
                self.print_help()
            raise e
        except CliError as e:
            error('CLI error: ' + str(e))
            raise e

    def print_help(self, *subcommands: str):
        print_help(self.__subrules, self.__name, self.__version, self.__help, *subcommands)

    def __add_default_rules(self):
        def __print_help(subcommands: List[str]):
            if not subcommands:
                subcommands = []
            self.print_help(*subcommands)

        def __print_version():
            print_version(self.__name, self.__version)

        def __bash_install(app_name: str):
            # TODO
            pass

        def __bash_autocomplete(cmdline: str):
            # TODO
            pass

        self.has(
            primary_option('-h', '--help', run=__print_help, help='Display this help and exit').has(
                all_arguments('subcommands'),
            ),
            primary_option('--version', run=__print_version, help='Print version information and exit'),
            primary_option('--bash-install', run=__bash_install,
                           help='install script as a bash binary and add autocompletion links').has(
                argument('app-name', help='binary name'),
            ),
            primary_option('--bash-autocomplete', run=__bash_autocomplete, help='return autocompletion list').has(
                all_arguments('cmdline', joined_with=' '),
            ),
            default_action(run=__print_help),
        )
