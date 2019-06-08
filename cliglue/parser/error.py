class CliError(RuntimeError):
    pass


class CliDefinitionError(CliError):
    pass


class ArgumentSyntaxError(CliError):
    pass
