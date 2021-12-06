from contextlib import contextmanager


class ContextError(RuntimeError):
    def __init__(self, message: str, **ctx):
        super().__init__(message)
        self.ctx = ctx


@contextmanager
def wrap_context(context_name: str, **ctx):
    try:
        yield
    except ContextError as e:
        merged_context = {**ctx, **e.ctx}
        raise ContextError(context_name, **merged_context) from e
    except Exception as e:
        raise ContextError(context_name, **ctx) from e
