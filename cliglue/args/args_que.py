from typing import List, Optional


class ArgsQue(object):
    def __init__(self, args: List[str]):
        self.__args = args
        self.__current_index = 0
        self.__next_index = 0

    def __iter__(self):
        return self.reset()

    def __next__(self) -> str:
        if self.has_next():
            self.__current_index = self.__next_index
            self.__next_index = self.__current_index + 1
            return self.__args[self.__current_index]
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self.__args)

    def __bool__(self) -> bool:
        return len(self.__args) > 0

    def has_next(self) -> bool:
        return self.__next_index < len(self.__args)

    def pop_current(self) -> str:
        current = self.__args.pop(self.__current_index)
        self.__next_index = self.__current_index
        return current

    def peek_current(self) -> Optional[str]:
        if self.__current_index >= len(self.__args):
            return None
        current = self.__args[self.__current_index]
        self.__next_index = self.__current_index + 1
        return current

    def pop_all(self) -> List[str]:
        all_args = self.__args
        self.__args = []
        self.reset()
        return all_args

    def reset(self) -> 'ArgsQue':
        self.__current_index = 0
        self.__next_index = 0
        return self
