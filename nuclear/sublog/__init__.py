from colorama import init

from .catch import logerr, ContextError
from .catch import logerr as log_error  # compatibility with deprecated API
from .context_logger import log, context_logger, root_context_logger
from .wrap_error import wrap_context

init()
