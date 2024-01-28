from colorama import init

from .catch import error_handler
from .sublog_logger import logger, log, log_exception, add_context
from .exception import exception_details, unwrap
from .context_error import ContextError

init()
