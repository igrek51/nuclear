def debug(message):
    print('\033[32m\033[1m[debug]\033[0m ' + str(message))


def info(message):
    print('\033[34m\033[1m[info]\033[0m  ' + str(message))


def warn(message):
    print('\033[33m\033[1m[warn]\033[0m  ' + str(message))


def error(message):
    print('\033[31m\033[1m[ERROR]\033[0m ' + str(message))


def fatal(message):
    error(message)
    raise RuntimeError(message)
