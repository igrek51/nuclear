from .builder.builder import CliBuilder
from .builder.rule_factory import subcommand, flag, dictionary, parameter, primary_option, argument, arguments, \
    default_action
from .shell.shell_utils import shell, sh, CommandError
from .shell.background_cmd import BackgroundCommand
from .sublog.catch import exception_handler
from .sublog.sublog_logger import logger, log, log_exception, add_context
from .sublog.exception import get_exception_details, unwrap
from .sublog.context_error import ContextError
from .inspection.inspection import inspect, wat, wats

from .version import __version__

name = "nuclear"
