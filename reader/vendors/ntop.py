from ..reader import FlowReader
import orjson

class CentoReader(FlowReader):

    def __init__(self, input):
        super().__init__(input)
        self.header = None
    
    def read(self):
        for row in self.input:
            if row.startswith('#'):
                continue
            data = orjson.loads(row)
            if self.header is None:
                self.header = data.keys()
            yield data
