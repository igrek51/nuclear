import os
import sys


def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8')


def save_file(file_path, content):
    f = open(file_path, 'wb')
    f.write(bytes(content, 'utf-8'))
    f.close()


def file_exists(path):
    return os.path.isfile(path)


def list_dir(path):
    return sorted(os.listdir(path))


def set_workdir(work_dir):
    os.chdir(work_dir)


def get_workdir():
    return os.getcwd()


def script_real_dir() -> str:
    return os.path.dirname(script_real_path())


def script_real_path() -> str:
    return os.path.realpath(sys.modules['__main__'].__file__)
