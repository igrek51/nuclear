import sys
from typing import Callable, List, Optional

from nuclear.autocomplete.autocomplete import bash_autocomplete
from nuclear.autocomplete.install import install_bash, install_autocomplete
from nuclear.builder.decorator_builder import create_decorated_subcommand
from nuclear.help.help import print_version, print_help, print_usage
from nuclear.parser.error import CliSyntaxError, CliDefinitionError
from nuclear.parser.parser import Parser
from nuclear.sublog import log
from nuclear.sublog.catch import logerr
from .rule import DefaultActionRule, CliRule, SubcommandRule
from .rule_factory import default_action, primary_option, arguments, argument, subcommand


class CliBuilder:
    def __init__(self,
                 name: Optional[str] = None,
                 version: Optional[str] = None,
                 help: Optional[str] = None,
                 run: Optional[Callable[..., None]] = None,
                 with_defaults: bool = True,
                 usage_onerror: bool = True,
                 reraise_error: bool = False,
                 hide_internal: bool = True,
                 help_on_empty: bool = False,
                 error_unrecognized: bool = True,
                 log_error: bool = False,
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
        --install-bash APP-NAME: installing application in bash with autocompleting,
        --autocomplete [CMDLINE...]: internal action for generating autocompleted proposals to be handled by bash
        :param usage_onerror: wheter usage output should be displayed on syntax error
        :param reraise_error: wheter syntax error should not be caught but reraised instead.
        Enabling this causes stack trace to be flooded to the user.
        :param hide_internal: wheter internal options (--install-bash, --autocomplete)
        should be hidden on help output.
        :param help_on_empty: shows help output when no argument is given
        :param error_unrecognized: raise error when unrecognized argument is found
        :param log_error: whether to catch exceptions and display traceback in a concise format
        """
        self.__name: str = name
        self.__version: str = version
        self.__help: str = help
        self.__subrules: List[CliRule] = []

        if run:
            self.has(default_action(run))

        self.__usage_onerror: bool = usage_onerror
        self.__reraise_error: bool = reraise_error
        self.__hide_internal: bool = hide_internal
        self.__help_on_empty: bool = help_on_empty
        self.__error_unrecognized: bool = error_unrecognized
        self.__log_error: bool = log_error
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
        if self.__log_error:
            with logerr():
                self.run_with_args(sys.argv[1:])
        else:
            self.run_with_args(sys.argv[1:])

    def run_with_args(self, args: List[str]):
        try:
            parser = self.__create_parser(args)
            parser.parse_args(args)
        except CliDefinitionError as e:
            log.error(f'CLI Definition error: {e}')
            raise e
        except CliSyntaxError as e:
            log.error(f'Syntax error: {e}')
            if self.__usage_onerror:
                self.print_usage()
            if self.__reraise_error:
                raise e

    def add_command(self, *subcommands: str):
        """
        Decorator for binding function with a CLI command
        :param subcommands: multi-part subcommand names composing the full command, eg. "git remote add"
        """
        def decorator(function):
            self.__bind_decorated_command(function, list(subcommands))

            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return decorator

    def __bind_decorated_command(self, function: Callable[..., None], names: List[str]):
        if not names:
            raise CliDefinitionError('subcommand name is required')
        if len(names) == 1:
            names = names[0].split(' ')

        last_rule = create_decorated_subcommand(function, names[-1])

        if len(names) == 1:
            self.has(last_rule)
        else:
            # first command added directly to the builder
            current_rule: SubcommandRule = self.__find_subcommand_rule(names[0])
            if not current_rule:
                current_rule = subcommand(names[0])
                self.has(current_rule)

            for subname in names[1:-1]:
                next_rule = _find_subcommand_rule(current_rule, subname)
                if not next_rule:
                    next_rule = subcommand(subname)
                    current_rule.has(next_rule)
                current_rule = next_rule    
                
            current_rule.has(last_rule)
    
    def __find_subcommand_rule(self, name: str) -> Optional[SubcommandRule]:
        for rule in self.__subrules:
            if isinstance(rule, SubcommandRule) and name in rule.keywords:
                return rule
        return None

    def __create_parser(self, args: List[str]) -> Parser:
        if not args and self.__help_on_empty:
            def __print_root_help():
                self.print_help([])

            return Parser([default_action(__print_root_help)])

        return Parser(self.__subrules, error_unrecognized=self.__error_unrecognized)

    def print_help(self, subcommands: List[str]):
        print_help(self.__subrules, self.__name, self.__version, self.__help, subcommands, self.__hide_internal)

    def print_usage(self):
        print_usage(self.__subrules)

    def __bash_autocomplete(self, cmdline: str, word_idx: Optional[int]):
        bash_autocomplete(self.__subrules, cmdline, word_idx)

    def __add_default_rules(self):
        def __print_root_help():
            self.print_help([])

        def __print_subcommand_help(subcommands: List[str]):
            self.print_help(subcommands)

        def __print_version():
            print_version(self.__name, self.__version)

        def __install_bash(app_name: str):
            install_bash(app_name)

        def __install_autocomplete(app_name: Optional[str]):
            install_autocomplete(app_name)

        def __bash_autocomplete(cmdline: str, word_idx: Optional[int]):
            self.__bash_autocomplete(cmdline, word_idx)

        if self.__version:
            self.has(
                primary_option('--version', run=__print_version, help='Print version information and exit'),
            )

        self.has(
            primary_option('-h', '--help', run=__print_subcommand_help, help='Display this help and exit').has(
                arguments('subcommands'),
            ),
            primary_option('--install-bash', run=__install_bash,
                           help='Install this program in bash to be executable from anywhere, '
                                'add autocompletion links').has(
                argument('app-name', help='binary name'),
            ),
            primary_option('--install-autocomplete', run=__install_autocomplete,
                           help='Install autocompletion links').has(
                argument('app-name', help='binary name', required=False),
            ),
            primary_option('--autocomplete', run=__bash_autocomplete,
                           help='Return matching autocompletion proposals').has(
                argument('cmdline', help='current command line'),
                argument('word-idx', help='current word index', type=int, required=False),
            ),
        )

        if not self.__has_default_action():
            self.has(default_action(__print_root_help))

    def __has_default_action(self) -> bool:
        return any([isinstance(rule, DefaultActionRule) for rule in self.__subrules])


def _find_subcommand_rule(subcommand_rule: SubcommandRule, name: str) -> Optional[SubcommandRule]:
    for rule in subcommand_rule.subrules:
        if isinstance(rule, SubcommandRule) and name in rule.keywords:
            return rule
    return None
