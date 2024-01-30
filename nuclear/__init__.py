from .cli.builder.builder import CliBuilder
from .cli.builder.rule_factory import subcommand, flag, dictionary, parameter, primary_option, argument, arguments, \
    default_action
from .shell.shell_utils import shell, shell_output, sh, CommandError
from .shell.background_cmd import BackgroundCommand
from .sublog.catch import error_handler
from .sublog.logging import logger, log, log_exception, add_context, get_logger, init_logs
from .sublog.exception import exception_details, unwrap
from .sublog.context_error import ContextError
from .inspection.inspection import wat

from .version import __version__

name = "nuclear"
