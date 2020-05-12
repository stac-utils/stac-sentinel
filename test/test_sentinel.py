import json
import unittest

from datetime import datetime as dt
import os.path as op

from stac_sentinel import sentinel_s2_l1c, sentinel_s2_l2a

testpath = op.dirname(__file__)


class Test(unittest.TestCase):
    """ Test main module """

    @classmethod
    def get_metadata(self, collection_id):
        with open(op.join(testpath, 'metadata', collection_id + '.json')) as f:
            dat = json.loads(f.read())
        return dat

    def test_sentinel_s2_l1c(self):
        collection_id = 'sentinel-s2-l1c'
        metadata = self.get_metadata(collection_id)
        item = sentinel_s2_l1c(metadata)
        fname = op.join(testpath, collection_id + '.json')
        with open(fname, 'w') as f:
            f.write(json.dumps(item))

    def test_sentinel_s2_l2a(self):
        collection_id = 'sentinel-s2-l2a'
        metadata = self.get_metadata(collection_id)
        item = sentinel_s2_l2a(metadata)
        fname = op.join(testpath, collection_id + '.json')
        with open(fname, 'w') as f:
            f.write(json.dumps(item))