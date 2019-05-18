from abc import ABC, abstractmethod

class Reader(ABC):
    def __init__(self, input):
        self.input = input
        self.hosts = set()
        
    @abstractmethod
    def read(self):
        pass


class FlowReader(Reader):
    def __init__(self, input):
        super().__init__(input)
        self.n_flows = 0
