# stac-sentinel

This repository is used for the creating [STAC Items](https://github.com/radiantearth/stac-spec) for [Sentinel remote sensing data](https://sentinel.esa.int) from their original metadata. Currently [Sentinel-1](https://sentinel.esa.int/web/sentinel/missions/sentinel-1) and [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) data is supported.

The library includes:

- STAC Collection metadata for [Sentinel-1 RTC](sentinel_to_stac/sentinel-s1-rtc.json), [Sentinel-2 L1C](sentinel_to_stac/sentinel-s2-l1c.json), and [Sentinel-2 L2A](sentinel_to_stac/sentinel-s2-l2a.json)
- Python functions for transforming the original metadata of a scene (tileInfo.json for Sentinel-2) into a STAC Item
- A Command Line Interface (CLI) for converting the original metadata files to STAC

## Public Catalogs

This library was used to index Sentinel-1 and Sentinel-2 data into a STAC API called Earth Search, available at:
https://www.element84.com/earth-search/

## Installation

If you are interested in using the library to create STAC Items from original metadata, you will need to install this library from GitHub. Because stac-sentinel uses PyProj, the [PROJ system libraries](https://proj.org/) will be needed as well and needs to be installed as per your system. You could also consider using the [GeoLambda](https://github.com/developmentseed/geolambda) base Docker image, which includes PROJ.

Then, to install the latest released version (from the `master` branch).

```
$ pip install git+https://github.com/stac-utils/stac-sentinel
```

To install a specific versions of stac-sentinel, install the matching version of stac-sentinel.

```bash
pip install git+https://github.com/stac-utils/stac-sentinel@v0.1.0
```

The table below shows the corresponding versions between stac-sentinel and STAC:

| stac-sentinel | STAC  |
| -------- | ----  |
| 0.1.0    | 1.0.0-beta1 |


## Usage

### Accessing Sentinel archive on AWS

### Command Line Interface

A command line tool is available for transforming an input metadata file into a STAC Item.

### Transforming individual scenes

The included functions allows one to transform the original metadata provided in GeoTIFFs (Sentinel-1) or tileInfo.json (Sentinel-2) into a STAC Item.

# transform a Sentinel-1 RTC scene
```
import rasterio
import json
from stac_sentinel import sentinel_s1_rtc

# get metadata
base_url = 's3://sentinel-s1-rtc-indigo/tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC'
with rasterio.open(base_url + '/local_incident_angle.tif') as src:
	metadata = src.profile
	metadata.update(src.tags())

# create an instance of SentinelSTAC for this scene (python dictionary)
item = sentinel_s1_rtc(metadata, base_url)

# write to local file
with open(item['id']+'.json', 'w') as f:
    f.write(json.dumps(item))

# optionally validate with pystac
import pystac
pystac.read_file(item['id']+'.json').validate() # KeyError: 'links' (relative links to collection, etc. not added automatically)
```
The `base_url` is the location, either local or remote, where the data for this scene can be found. In the case above, the data is staged locally, so the base_url is given as just the current directory, where it will look for the asset data files expected (as provided in the original metadata).  

If the data is remote, then reading it for a scene would look different:

# transform a Sentinel-2 L1C scene
```
import requests
import json
from stac_sentinel import sentinel_s2_l1c

# get tileInfo
url = 'https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/17/T/KE/2015/10/23/0/tileInfo.json'
r = requests.get(url, stream=True)
metadata = json.loads(r.text)

# create an instance of SentinelSTAC for this scene
item = sentinel_s2_l1c(metadata, base_url='s3://sentinel-s2-l1c/tiles/17/T/KE/2015/10/23/0')
```

Note however that in this example, the base_url of s3://sentinel-s2-l1c, is a requester-pays bucket. It will be used to generate the links to the assets as seen in the [Sentinel-2 L1C example](samples/sentinel-s2-l1c_item.json), but none of these files are accessed directly.

However, for Sentinel-1, there is an additional metadata file that is needed that is only available in the bucket. **If you have credentials defined when running this code, it will automatically use requester-pays and you will be charged!**


## STAC conversion notes

### Sentinel-1

Sentinel-1 RTC images are derived from multiple Sentinel-1 GRD frames. Full documentation here: https://registry.opendata.aws/sentinel-1-rtc-indigo/. We extract key metadata stored as GEOTIFF tags in `local_incident_angle.tif`. Additional extensive metadata from the GRDs are available `manifest.safe` and `productInfo.json`. An example folder structure looks like the following for `s3://sentinel-s1-rtc-indigo/tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC`:
```
.
├── Gamma0_VH.tif
├── Gamma0_VV.tif
├── README.txt
├── S1B_IW_GRDH_1SDV_20161121T010910_20161121T010939_003050_0052FC_EC22
│   ├── manifest.safe
│   └── productInfo.json
├── S1B_IW_GRDH_1SDV_20161121T010939_20161121T011004_003050_0052FC_3426
│   ├── manifest.safe
│   └── productInfo.json
└── local_incident_angle.tif
```

### Sentinel-2

The tileInfo.json contains all of the data needed to create a STAC Item, however the given geometry is in native coordinates rather than lat/lon. The library reprojects the geometry using EPSG:4326. Additionally, the convex hull is calculated for the geometry. In most cases this doesn't make a difference, however some of the tile geometries can be long and complex. Taking the convex hull is a way to simplify the geometry without impacting search and discovery.

## Development

The `master` branch is the latest versioned release, while the `develop` branch is the latest development version. When making a new release:

- Update the [version](stac_sentinel/version.py)
- Update [CHANGELOG.md](CHANGELOG.md)
- Create PR and merge to master
- Create a release on GitHub from `master` with the new version

## About
[stac_sentinel](https://github.com/stac-utils/stac-sentinel) leverages the use of [Spatio-Temporal Asset Catalogs](https://github.com/radiantearth/stac-spec)
