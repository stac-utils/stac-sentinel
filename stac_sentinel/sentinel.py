import json
import logging
import os.path as op

from dateutil.parser import parse
from pyproj import Proj, transform as reproj
from shapely import geometry
from .version import __version__, __stac_version__

logger = logging.getLogger(__name__)


def get_collection(collection_id):
    """ Get STAC Collection JSON """
    filename = op.join(op.dirname(__file__), '%s.json' % collection_id)
    collection = json.loads(open(filename).read())
    return collection


def sentinel_s2(metadata):
    """ Parse tileInfo.json and return basic Item """
    dt = parse(metadata['timestamp'])
    # geometry - TODO see about getting this from a productInfo file without having to reproject
    epsg = metadata['tileOrigin']['crs']['properties']['name'].split(':')[-1]
    native_coordinates = metadata['tileDataGeometry']['coordinates']
    ys = [c[1] for c in native_coordinates[0]]
    xs = [c[0] for c in native_coordinates[0]]
    p1 = Proj(init='epsg:%s' % epsg)
    p2 = Proj(init='epsg:4326')
    lons, lats = reproj(p1, p2, xs, ys)
    bbox = [min(lons), min(lats), max(lons), max(lats)]
    coordinates = [[[lons[i], lats[i]] for i in range(0, len(lons))]]
    geom = geometry.mapping(geometry.Polygon(coordinates[0]).convex_hull)

    # Item properties
    props = {
        'datetime': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'platform': 'sentinel-2%s' % metadata['productName'][2].lower(),
        'constellation': 'sentinel-2',
        'instruments': ['msi'],
        'gsd': 10,
        'view:off_nadir': 0,
        'proj:epsg': int(epsg),
        'sentinel:latitude_band': metadata['latitudeBand'],
        'sentinel:grid_square': metadata['gridSquare'],
        'sentinel:sequence': metadata['path'].split('/')[-1],
        'sentinel:product_id': metadata['productName']
    }
    if 'dataCoveragePercentage' in metadata:
        props['sentinel:data_coverage'] = float(metadata['dataCoveragePercentage'])
    if 'cloudyPixelPercentage' in metadata:
        props['eo:cloud_cover'] = float(metadata['cloudyPixelPercentage'])

    sid = str(metadata['utmZone']) + metadata['latitudeBand'] + metadata['gridSquare']
    level = metadata['datastrip']['id'].split('_')[3]
    id = '%s_%s_%s_%s_%s' % (metadata['productName'][0:3], sid,
                                dt.strftime('%Y%m%d'), props['sentinel:sequence'], level)
    item = {
        'type': 'Feature',
        'stac_version': __stac_version__,
        'stac_extensions': ['eo', 'view', 'proj'],
        'id': id,
        'bbox': bbox,
        'geometry': geom,
        'properties':props
    }
    return item


def sentinel_s2_l1c(metadata, base_url=''):
    collection_id = 'sentinel-s2-l1c'
    item = sentinel_s2(metadata)
    item['collection'] = collection_id
    assets = get_collection(collection_id)['item_assets']
    assets['thumbnail']['href'] = op.join(base_url, 'preview.jpg')
    assets['info']['href'] = op.join(base_url, 'tileInfo.json')
    assets['metadata']['href'] = op.join(base_url, 'metadata.xml')
    assets['overview']['href'] = op.join(base_url, 'TCI.jp2')
    assets['B01']['href'] = op.join(base_url, 'B01.jp2')
    assets['B02']['href'] = op.join(base_url, 'B02.jp2')
    assets['B03']['href'] = op.join(base_url, 'B03.jp2')
    assets['B04']['href'] = op.join(base_url, 'B04.jp2')
    assets['B05']['href'] = op.join(base_url, 'B05.jp2')
    assets['B06']['href'] = op.join(base_url, 'B06.jp2')
    assets['B07']['href'] = op.join(base_url, 'B07.jp2')
    assets['B08']['href'] = op.join(base_url, 'B08.jp2')
    assets['B8A']['href'] = op.join(base_url, 'B8A.jp2')
    assets['B09']['href'] = op.join(base_url, 'B09.jp2')
    assets['B10']['href'] = op.join(base_url, 'B10.jp2')
    assets['B11']['href'] = op.join(base_url, 'B11.jp2')
    assets['B12']['href'] = op.join(base_url, 'B12.jp2')
    item['assets'] = assets
    # remove some asset properties that are defined at collection
    for key in assets:
        assets[key].pop('description', None)
        assets[key].pop('eo:bands', None)
        assets[key].pop('gsd', None)
        assets[key].pop('roles', None)
    return item


def sentinel_s2_l2a(metadata, base_url=''):
    collection_id = 'sentinel-s2-l2a'
    item = sentinel_s2(metadata)
    item['collection'] = collection_id
    assets = get_collection(collection_id)['item_assets']
    # get link back to l1c data
    s2_l1c_base_url = base_url.replace('sentinel-s2-l2a', 'sentinel-s2-l1c')
    assets['thumbnail']['href'] = op.join(s2_l1c_base_url, 'preview.jpg')
    assets['info']['href'] = op.join(base_url, 'tileInfo.json')
    assets['metadata']['href'] = op.join(base_url, 'metadata.xml')
    assets['overview']['href'] = op.join(base_url, 'qi/L2A_PVI.jp2')
    assets['visual']['href'] = op.join(base_url, 'R10m/TCI.jp2')
    assets['B02']['href'] = op.join(base_url, 'R10m/B02.jp2')
    assets['B03']['href'] = op.join(base_url, 'R10m/B03.jp2')
    assets['B04']['href'] = op.join(base_url, 'R10m/B04.jp2')
    assets['B08']['href'] = op.join(base_url, 'R10m/B08.jp2')
    assets['AOT']['href'] = op.join(base_url, 'R60m/AOT.jp2')
    assets['WVP']['href'] = op.join(base_url, 'R10m/WVP.jp2')
    assets['visual_20m']['href'] = op.join(base_url, 'R20m/TCI.jp2')
    assets['B05']['href'] = op.join(base_url, 'R20m/B05.jp2')
    assets['B06']['href'] = op.join(base_url, 'R20m/B06.jp2')
    assets['B07']['href'] = op.join(base_url, 'R20m/B07.jp2')
    assets['B8A']['href'] = op.join(base_url, 'R20m/B8A.jp2')
    assets['B11']['href'] = op.join(base_url, 'R20m/B11.jp2')
    assets['B12']['href'] = op.join(base_url, 'R20m/B12.jp2')
    assets['SCL']['href'] = op.join(base_url, 'R20m/SCL.jp2')
    assets['visual_60m']['href'] = op.join(base_url, 'R60m/TCI.jp2')
    assets['B01']['href'] = op.join(base_url, 'R60m/B01.jp2')
    assets['B09']['href'] = op.join(base_url, 'R60m/B09.jp2')
    # remove some asset properties that are defined at collection
    for key in assets:
        assets[key].pop('description', None)
        assets[key].pop('eo:bands', None)
        assets[key].pop('gsd', None)
        assets[key].pop('roles', None)
    item['assets'] = assets
    return item
