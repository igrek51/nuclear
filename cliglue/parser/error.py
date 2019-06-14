class CliError(RuntimeError):
    pass


class CliDefinitionError(CliError):
    def __init__(self, msg: str):
        super().__init__('CLI Definition error: ' + msg)


class CliSyntaxError(CliError):
    def __init__(self, msg: str):
        super().__init__('Syntax error: ' + msg)
