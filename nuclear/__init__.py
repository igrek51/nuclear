from .builder.builder import CliBuilder
from .builder.rule_factory import subcommand, flag, dictionary, parameter, primary_option, argument, arguments, \
    default_action
from .shell.shell_utils import shell, shell_error_code, shell_output, CommandError
from .shell.background_cmd import BackgroundCommand
from .sublog.catch import logerr, ContextError, log_exception
from .sublog.context_logger import log
from .sublog.wrap_error import wrap_context
from .inspection.inspection import inspect, ins, insp, insl, insa

from .version import __version__

name = "nuclear"
