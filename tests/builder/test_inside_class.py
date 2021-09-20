from nuclear import CliBuilder
from tests.asserts import MockIO


class Classy:
    def helpme(self):
        print(f'{self.extra} helpme')
    
    def builder(self):
        self.extra = 'pls'
        return CliBuilder(run=self.helpme)


def test_bind_with_class_method():
    with MockIO() as mockio:
        Classy().builder().run()
        assert mockio.stripped() == 'pls helpme'
