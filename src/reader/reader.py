import sys
import urllib
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
    def src_ipv4(self):
        return self.config['fields']['ip']['v4']['src']

    @property
    def dst_ipv4(self):
        return self.config['fields']['ip']['v4']['dst']

    @property
    def dst_ipv6(self):
        return self.config['fields']['ip']['v6']['dst']

    @property
    def src_ipv6(self):
        return self.config['fields']['ip']['v6']['src']

    def _hosts(self, data):
        try:
            return '{}_{}'.format(data[self.src_mac], data[self.src_ipv4 if self.src_ipv4 in data else self.src_ipv6]), '{}_{}'.format(data[self.dst_mac], data[self.dst_ipv4 if self.dst_ipv4 in data else self.dst_ipv6])
        except KeyError as e:
            print(e)


class JsonFlowReader(FlowReader):

    @staticmethod
    def _quote_url(row):
        start = row.find('"HTTP_URL":')
        # try to fix http url
        if start > -1:
            start += len('"HTTP_URL":')
            start += row[start:].find('"') + 1
            end = start + (row[start:].find('","') if row[start:].find('","') != -1 else row[start:].find('"}'))
            http_url_quoted = urllib.parse.quote_plus(row[start:end])
            row = row.replace(row[start:end], http_url_quoted)
        return row

    def read(self):
        for i, row in enumerate(self.input):
            if not row or row.startswith('#'):
                continue
            row = self._quote_url(row)
            data = orjson.loads(row)
            if self.header is None:
                self.header = data.keys()
            self.n_flows += 1
            for h in self._hosts(data):
                self.hosts.add(h)
            yield data

    def hosts2flow(self):
        hosts2data = {}
        for flow in self.read():
            src, dst = self._hosts(flow)
            for h in (src, dst):
                if h not in hosts2data:
                    hosts2data[h] = []
                hosts2data[h].append(flow)
        return hosts2data