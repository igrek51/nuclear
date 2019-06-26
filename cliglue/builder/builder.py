import sys
from typing import Any, List, Optional

from cliglue.autocomplete.autocomplete import bash_install, bash_autocomplete
from cliglue.help.help import print_version, print_help
from cliglue.parser.error import CliSyntaxError, CliDefinitionError
from cliglue.parser.parser import Parser
from cliglue.utils.output import error
from .rule import SubcommandRule, PrimaryOptionRule, ParameterRule, PositionalArgumentRule, AllArgumentsRule, \
    DefaultActionRule, FlagRule, CliRule
from .typedef import Action, ChoiceProvider, TypeOrParser


def subcommand(
        *keywords: str,
        run: Optional[Action] = None,
        help: str = None,
) -> SubcommandRule:
    """
    Create Subcommand rule specification.
    Subcommand is a keyword which narrows down the context and can execute an action.
    Subcommands may build a tree.
    :param keywords: keyword arguments which trigger subcommand
    :param run: optional action to be invoked when subcommand is matched
    :param help: description of the subcommand
    :return: new subcommand rule specification
    """
    return SubcommandRule(help, set(keywords), run)


def flag(
        *keywords: str,
        help: str = None,
) -> FlagRule:
    """
    TODO
    :param keywords:
    :param help:
    :return: new flag rule specification
    """
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
    """
    TODO

    :param keywords:
    :param name:
    :param help:
    :param required:
    :param default:
    :param type:
    :param choices:
    :return: new parameter rule specification
    """
    return ParameterRule(set(keywords), name, required, default, type, choices, help)


def primary_option(
        *keywords: str,
        run: Action = None,
        help: str = None,
) -> PrimaryOptionRule:
    """
    TODO
    :param keywords:
    :param run:
    :param help:
    :return: new primary option rule specification
    """
    return PrimaryOptionRule(help, set(keywords), run)


def argument(
        name: str,
        help: str = None,
        required: bool = True,
        default: Any = None,
        type: TypeOrParser = str,
        choices: ChoiceProvider = None,
) -> PositionalArgumentRule:
    """
    TODO

    :param name:
    :param help:
    :param required:
    :param default:
    :param type:
    :param choices:
    :return: new positional argument rule specification
    """
    return PositionalArgumentRule(name, required, default, type, choices, help)


def all_arguments(
        name: str,
        joined_with: Optional[str] = None,
) -> AllArgumentsRule:
    """
    TODO

    :param name:
    :param joined_with:
    :return: new all remaining arguments rule specification
    """
    return AllArgumentsRule(name, joined_with)


def default_action(
        run: Action = None,
) -> DefaultActionRule:
    """
    TODO

    :param run:
    :return: new default action specification
    """
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
        """
        A builder for Command Line Interface specification
        :param name: name of the application for which the CLI is built
        :param version: application version (displayed in help/version output)
        :param help: short description of application
        :param run: reference for a function which should be the default action for empty arguments list
        :param with_defaults: whether default rules and actions should be added.
        Defaults options are:
        -h, --help: displaying help,
        --version: displaying version,
        --bash-install APP-NAME: installing application in bash with autocompleting,
        --bash-autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash
        :param help_onerror: wheter help output should be displayed on syntax error
        :param reraise_error: wheter syntax error should not be caught but reraised instead.
        Enabling this causes stack trace to be flooded to the user.
        """
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
        """
        Add more CLI rules for the particular level
        :param subrules: Command Line Interface rules,
        such as: subcommands, flags, parameters, options, arguments, default action
        :return: CliBuilder itself for the further building
        """
        self.__subrules += subrules
        return self

    def run(self):
        """
        Parse all the CLI arguments passed to application.
        Then invoke triggered action which were defined before.
        If actions need some parameters, they will be injected based on the parsed arguments.
        """
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

    def __bash_autocomplete(self, cmdline: str):
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
            self.__bash_autocomplete(cmdline)

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
