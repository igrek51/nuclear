import os
import sys


def script_real_path() -> str:
    return os.path.realpath(sys.modules['__main__'].__file__)
