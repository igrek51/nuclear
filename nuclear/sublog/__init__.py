from colorama import init

from .catch import exception_handler
from .sublog_logger import logger, log, log_exception, add_context
from .exception import get_exception_details, unwrap
from .context_error import ContextError

init()
