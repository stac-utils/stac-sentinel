# sentinel-to-stac

This repository is used for the creating [STAC Items](https://github.com/radiantearth/stac-spec) for [Sentinel remote sensing data](https://sentinel.esa.int) from their original metadata. Currently [Sentinel-1](https://sentinel.esa.int/web/sentinel/missions/sentinel-1) and [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) data is supported.

The library includes:

- STAC Collection metadata for [Sentinel-1 L1C](sentinel_to_stac/sentinel-s1-l1c.json), [Sentinel-2 L1C](sentinel_to_stac/sentinel-s2-l1c.json), and [Sentinel-2 L2A](sentinel_to_stac/sentinel-s2-l2a.json)
- Python functions for transforming the original metadata of a scene (productInfo.json for Sentinel-1, tileInfo.json for Sentinel-2) into a STAC Item. See [sample Items](samples/)
- A Command Line Interface (CLI) for converting the original metadata files to STAC


## Table of Contents

- [sentinel-to-stac](#sentinel-to-stac)
  - [Table of Contents](#table-of-contents)
  - [Public Catalogs](#public-catalogs)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Accessing Sentinel archive on AWS](#accessing-sentinel-archive-on-aws)
    - [Command Line Interface](#command-line-interface)
    - [Transforming individual scenes](#transforming-individual-scenes)
- [transform a Sentinel-2 L1C scene](#transform-a-sentinel-2-l1c-scene)
- [get tileInfo](#get-tileinfo)
- [create an instance of SentinelSTAC for this scene](#create-an-instance-of-sentinelstac-for-this-scene)
  - [STAC conversion notes](#stac-conversion-notes)
    - [Sentinel-1](#sentinel-1)
    - [Sentinel-2](#sentinel-2)
  - [Development](#development)
  - [About](#about)


## Public Catalogs

This library was used to index Sentinel-1 and Sentinel-2 data into a STAC API called Earth Search, available at:


## Installation

If you are interested in using the library to create STAC Items from original metadata, you will need to install this library from GitHub. Because stac-sentinel uses PyProj, the [PROJ system libraries](https://proj.org/) will be needed as well and needs to be installed as per your system. You could also consider using the [GeoLambda](https://github.com/developmentseed/geolambda) base Docker image, which includes PROJ.

Then, to install the latest released version (from the `master` branch).

```
$ pip install git+https://github.com/stac-utils/sentinel_to_stac
```

To install a specific versions of stac-sentinel, install the matching version of stac-sentinel. 

```bash
pip install git+https://github.com/stac-utils/sentinel_to_stac@0.0.1
```

The table below shows the corresponding versions between stac-sentinel and STAC:

| stac-sentinel | STAC  |
| -------- | ----  |
| 0.0.1    | 1.0.0-beta1 |


## Usage

### Accessing Sentinel archive on AWS

### Command Line Interface

A command line tool is available for transforming an input metadata file into a STAC Item.

### Transforming individual scenes

The included functions allows one to transform the original metadata provided in productInfo.json (Sentinel-1) or tileInfo.json (Sentinel-2) into a STAC Item.

```
# transform a Sentinel-1 L1C scene

The `base_url` is the location, either local or remote, where the data for this scene can be found. In the case above, the data is staged locally, so the base_url is given as just the current directory, where it will look for the asset data files expected (as provided in the original metadata).  

If the data is remote, then reading it for a scene would look different:

```
# transform a Sentinel-2 L1C scene

import requests
import json
from sentinel_to_stac import sentinel_s2_l1c

# get tileInfo
url = 'https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/17/T/KE/2015/10/23/0/tileInfo.json'
r = requests.get(url, stream=True)
metadata = json.loads(r.text)

# create an instance of SentinelSTAC for this scene
item = sentinel_s2_l1c(metadata, base_url='s3://sentinel-s2-l1c/tiles/17/T/KE/2015/10/23/0')


Note however that in this example, the base_url of s3://sentinel-s2-l1c, is a requester-pays bucket. It will be used to generate the links to the assets as seen in the [Sentinel-2 L1C example](samples/sentinel-s2-l1c_item.json), but none of these files are accessed directly.

However, for Sentinel-1, there is an additional metadata file that is needed that is only available in the bucket. **If you have credentials defined when running this code, it will automatically use requester-pays and you will be charged!** 


## STAC conversion notes

### Sentinel-1

The main metadata for a Sentinel-1 scene is contained in the `productInfo.json` file, but it does not contain all metadata needed. For each Sentinel-1 asset in the scene there is an XML annotation file (in the annotation/ subdirectory). Most of the data in the annotation file is the same across all annotation files within the scene, so only a single one is needed (there is asset specific data including statistics and noise estimates that are not needed). This annotation file is fetched, and usedto fill in the additional STAC metadata.

### Sentinel-2

The tileInfo.json contains all of the data needed to create a STAC Item, however the given geometry is in native coordinates rather than lat/lon. The library reprojects the geometry using EPSG:4326. Additionally, the convex hull is calculated for the geometry. In most cases this doesn't make a difference, however some of the tile geometries can be long and complex. Taking the convex hull is a way to simplify the geometry without impacting search and discovery.

## Development

The `master` branch is the latest versioned release, while the `develop` branch is the latest development version. When making a new release:

- Update the [version](stac_sentinel/version.py)
- Update [CHANGELOG.md](CHANGELOG.md)
- Create PR and merge to master
- Create a release on GitHub from `master` with the new version

## About
[stac_sentinel](https://github.com/stac-utils/sentinel-to-stac) leverages the use of [Spatio-Temporal Asset Catalogs](https://github.com/radiantearth/stac-spec)
