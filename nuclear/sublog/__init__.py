from colorama import init

from .catch import error_handler
from .sublog_logger import logger, log, log_exception, add_context, get_logger, init_logs
from .exception import exception_details, unwrap
from .context_error import ContextError

init()
init_logs()
