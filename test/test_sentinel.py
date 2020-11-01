import json
import unittest

from datetime import datetime as dt
import os.path as op
import rasterio
from stac_sentinel import sentinel_s2_l1c, sentinel_s2_l2a, sentinel_s1_rtc
import pystac
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

    def test_sentinel_s1_rtc(self):
        collection_id = 'sentinel-s1-rtc'
        with rasterio.open(op.join(testpath, 'metadata', collection_id + '.tif')) as src:
            metadata = src.profile
            metadata.update(src.tags())
        item = sentinel_s1_rtc(metadata)
        fname = op.join(testpath, collection_id + '.json')
        with open(fname, 'w') as f:
            f.write(json.dumps(item))

    def validate_sentinel_s1_rtc_collection(self):
        collection_id = 'sentinel-s1-rtc'
        fname = f'../stac_sentinel/{collection_id}.json'
        collection = pystac.read_file(fname)
        collection.validate()

    def validate_sentinel_s1_rtc_item(self):
        collection_id = 'sentinel-s1-rtc'
        fname = op.join(testpath, collection_id + '.json')
        item = pystac.read_file()
        item.validate()
