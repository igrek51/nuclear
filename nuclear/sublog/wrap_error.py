from contextlib import contextmanager


class ContextError(RuntimeError):
    def __init__(self, message: str, **ctx):
        super().__init__(message)
        self.context_message = message
        self.ctx = ctx

    def __str__(self):
        return _error_message(self)


def _error_message(e: Exception):
    layers = []
    while e is not None:
        if isinstance(e, ContextError):
            layers.append(e.context_message)
        else:
            layers.append(str(e))
        e = e.__cause__
    return ': '.join(layers)


@contextmanager
def wrap_context(context_name: str, **ctx):
    try:
        yield
    except ContextError as e:
        merged_context = {**ctx, **e.ctx}
        raise ContextError(context_name, **merged_context) from e
    except Exception as e:
        raise ContextError(context_name, **ctx) from e
