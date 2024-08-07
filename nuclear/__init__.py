from .cli.builder.builder import CliBuilder
from .cli.builder.rule_factory import subcommand, flag, dictionary, parameter, primary_option, argument, arguments, \
    default_action
from .shell.shell_utils import shell, shell_output, sh, CommandError
from .shell.background_cmd import BackgroundCommand
from .sublog.catch import error_handler
from .sublog.logging import logger, log, log_exception, add_context, get_logger, init_logs
from .sublog.exception import exception_details, unwrap
from .sublog.context_error import ContextError

from .version import __version__

name = "nuclear"

__all__ = [
    'CliBuilder',
    'subcommand', 'flag', 'dictionary', 'parameter', 'primary_option', 'argument', 'arguments', 'default_action',
    'shell', 'shell_output', 'sh', 'CommandError',
    'BackgroundCommand',
    'error_handler',
    'logger', 'log', 'log_exception', 'add_context', 'get_logger', 'init_logs',
    'exception_details', 'unwrap',
    'ContextError',
]
