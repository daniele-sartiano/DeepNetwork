import os
import unittest
from .. import ntop

class TestCentoReader(unittest.TestCase):
    path = os.path.dirname(os.path.realpath(__file__))
    data = os.path.join(path, 'data', 'sample_ntop_cento.txt')

    def test_read(self):

        with open(self.data) as f:
            reader = ntop.CentoReader(f)
            data = [el for el in reader.read()]
            f.seek(0)
            nlines = f.readlines()
        self.assertEqual(len(data), len(nlines)-1)

        headers_len = set([len(el.keys()) for el in data])
        self.assertEqual(1, len(headers_len))
        self.assertEqual(headers_len.pop(), len(reader.header))

if __name__ == '__main__':
    unittest.main()
