from typing import List


class ArgsQue(object):
    def __init__(self, args: List[str]):
        self.__args = args
        self.__index = -1

    def __iter__(self):
        return self.reset()

    def __next__(self) -> str:
        if self.has_next():
            self.__index += 1
            return self.__args[self.__index]
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self.__args)

    def __bool__(self) -> bool:
        return len(self.__args) > 0

    def has_next(self) -> bool:
        return self.__index + 1 < len(self.__args)

    def pop_current(self) -> str:
        current = self.__args.pop(self.__index)
        self.__index -= 1
        return current

    def pop_all(self) -> List[str]:
        all_args = self.__args
        self.__args = []
        self.__index = -1
        return all_args

    def reset(self) -> 'ArgsQue':
        self.__index = -1
        return self
