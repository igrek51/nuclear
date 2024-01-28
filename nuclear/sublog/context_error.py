from typing import Dict, Any


class ContextError(RuntimeError):
    """
    Error wrapping other error, adding context message
    and printing it in a Go manner - from most general to the real cause,
    eg: 'initializing app: loading config: file is missing'

    Usage:
        try:
            raise RuntimeError('file is missing')
        except Exception as e:
            raise ContextError('loading config') from e
    """

    def __init__(self, context_message: str, cause: BaseException | None = None, **ctx):
        super().__init__()
        self.context_message: str = context_message
        self.ctx: Dict[str, Any] = ctx
        if cause is not None:
            self.__cause__ = cause

    def __str__(self):
        if self.__cause__ is None:
            return self.context_message
        else:
            return f'{self.context_message}: {self.__cause__}'
