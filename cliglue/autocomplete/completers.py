import os


def file_completer():
    names = []
    for file in [f for f in os.listdir('.')]:
        if os.path.isdir(file):
            names.append(f'{file}/')
        else:
            names.append(file)
    return sorted(names)
