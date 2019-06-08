from cliglue import types
from cliglue.builder import *


def say_hello(name: str, surname: str, force: bool):
    print('Hello {} {}'.format(name, surname))
    if force:
        print('May the Force be with you!')


def main():
    CliBuilder('multiapp').has(
		argument('name'),
		argument('surname', required=False),
    	flag('force'),
    ).run()


if __name__ == '__main__':
    main()
