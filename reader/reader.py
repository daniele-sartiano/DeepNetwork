from abc import ABC, abstractmethod

class Reader(ABC):
    def __init__(self, input):
        self.input = input

    @abstractmethod
    def read(self):
        pass


class FlowReader(Reader):
    pass
