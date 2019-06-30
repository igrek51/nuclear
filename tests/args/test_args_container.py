from cliglue import *
from cliglue.args.container import ArgsContainer
from tests.asserts import MockIO, assert_error


def test_args_container_by_attr():
    def print_args_dict(args):
        print(' '.join([
            args.param, args.p,
            str(args.p2),
            args.multi_ple_words,
            args.nnn,
        ]))

    with MockIO('--param', 'pval', '--multi-ple-words', 'words', '--p2', '--named-param=mmm') as mockio:
        CliBuilder(run=print_args_dict).has(
            parameter('param', '-p'),
            flag('p2'),
            parameter('multi-ple-words'),
            parameter('named-param', name='nnn'),
        ).run()
        assert mockio.stripped_output() == 'pval pval True words mmm'


def test_args_container_by_dict_name():
    def print_args_dict(args):
        print(' '.join([
            args['param'], args['--param'], args['p'], args['-p'],
            str(args['p2']), str(args['--p2']),
            args['multi-ple-words'], args['multi_ple_words'],
            args['nnn'],
        ]))

    with MockIO('--param', 'pval', '--multi-ple-words', 'words', '--p2', '--named-param=mmm') as mockio:
        CliBuilder(run=print_args_dict).has(
            parameter('param', '-p'),
            flag('p2'),
            parameter('multi-ple-words'),
            parameter('named-param', name='nnn'),
        ).run()
        assert mockio.stripped_output() == 'pval pval pval pval True True words words mmm'


def test_args_container_error_on_nonexisting():
    def get_notexisting(args):
        assert_error(lambda: print(args['no_attr']), KeyError)
        assert_error(lambda: print(args.no_such_attr), AttributeError)

    with MockIO('-f'):
        CliBuilder(run=get_notexisting).has(
            flag('f'),
        ).run()


def test_shadowed_args_container_var():
    def print_it(args: ArgsContainer):
        print(args.f)

    with MockIO() as mockio:
        CliBuilder(run=print_it).has(
            flag('f'),
        ).run()
        assert mockio.output() == 'False\n'
