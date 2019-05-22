import os
import unittest
from .. import reader


class TestJsonFlowReader(unittest.TestCase):
    path = os.path.dirname(os.path.realpath(__file__))
    data = os.path.join(path, 'data', 'sample_json_flow.txt')
    config = os.path.join(path, 'conf', 'json_flow.yaml')
    
    def test_read(self):
        with open(self.data) as f:
            r = reader.JsonFlowReader(f, self.config)
            data = [el for el in r.read()]
            f.seek(0)
            nlines = f.readlines()
        self.assertEqual(len(data), len(nlines)-1)

        headers_len = set([len(el.keys()) for el in data])
        self.assertEqual(1, len(headers_len))
        self.assertEqual(headers_len.pop(), len(r.header))


if __name__ == '__main__':
    unittest.main()
