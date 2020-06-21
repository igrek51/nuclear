import os


def file_completer():
    files = [f for f in os.listdir('.')]
    return sorted(files)
