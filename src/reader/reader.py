from abc import ABC, abstractmethod
import orjson
import yaml

class Reader(ABC):
    def __init__(self, input):
        self.input = input
        self.hosts = set()
        
    @abstractmethod
    def read(self):
        pass


class FlowReader(Reader):
    def __init__(self, input, config):
        super().__init__(input)
        self.n_flows = 0
        self.header = None
        with open(config) as f:
            self.config = yaml.load(f.read(), yaml.Loader)
        
    @property
    def src_mac(self):
        return self.config['fields']['mac']['src']

    @property
    def dst_mac(self):
        return self.config['fields']['mac']['dst']

    @property
    def src_ip(self):
        return self.config['fields']['ip']['src']

    @property
    def dst_ip(self):
        return self.config['fields']['ip']['dst']

    def _hosts(self, data):
        return '{}_{}'.format(data[self.src_mac], data[self.src_ip]), '{}_{}'.format(data[self.dst_mac], data[self.dst_ip])


class JsonFlowReader(FlowReader):
    def read(self):
        for row in self.input:
            if row.startswith('#'):
                continue
            data = orjson.loads(row)
            if self.header is None:
                self.header = data.keys()
            self.n_flows += 1
            for h in self._hosts(data):
                self.hosts.add(h)
            yield data

