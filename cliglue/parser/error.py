class CliError(RuntimeError):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg

    def __str__(self):
        if self.__cause__:
            return f'{self.__msg}: {self.__cause__}'
        return self.__msg


class CliDefinitionError(CliError):
    def __init__(self, msg: str):
        super().__init__(msg)


class CliSyntaxError(CliError):
    def __init__(self, msg: str):
        super().__init__(msg)
