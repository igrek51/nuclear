from typing import Dict, Any, Optional


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

    def __init__(self, context_message: str, cause: Optional[BaseException] = None, **ctx):
        super().__init__()
        self.context_message: str = context_message
        self.ctx: Dict[str, Any] = ctx
        if cause is not None:
            self.__cause__ = cause

    def __str__(self) -> str:
        e: Exception = self
        layers = []
        while e is not None:
            if isinstance(e, ContextError):
                layers.append(e.context_message)
            else:
                layers.append(str(e))
            e = e.__cause__
        return ': '.join(layers)
