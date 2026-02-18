# Data Sources Documentation

## Overview
This document details all the data sources used in the Salish Sea Watershed mapping project.

## 1. Natural Earth Data

### Description
Natural Earth is a public domain map dataset available at multiple scales. We use the 1:10m (1:10 million) scale for detailed regional mapping.

### Datasets Used

#### Coastlines (ne_10m_coastline)
- **URL:** https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-coastline/
- **Format:** Shapefile (SHP)
- **License:** Public Domain
- **Description:** Global coastline data suitable for regional mapping
- **Usage:** Defining the Salish Sea shoreline and islands

#### Rivers and Lake Centerlines (ne_10m_rivers_lake_centerlines)
- **URL:** https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-rivers-lake-centerlines/
- **Format:** Shapefile (SHP)
- **License:** Public Domain
- **Description:** Major rivers and streams worldwide
- **Usage:** Showing major rivers flowing into the Salish Sea

#### Lakes (ne_10m_lakes)
- **URL:** https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-lakes/
- **Format:** Shapefile (SHP)
- **License:** Public Domain
- **Description:** Large lakes and water bodies
- **Usage:** Context for the regional hydrology

## 2. OpenStreetMap (OSM)

### Description
OpenStreetMap is a collaborative mapping project creating free editable maps of the world.

### Access Method
We use the Overpass API to query specific features within the Salish Sea bounding box.

#### Overpass API
- **URL:** https://overpass-api.de/api/interpreter
- **License:** ODbL (Open Database License)
- **Rate Limit:** Reasonable use policy (queries should complete within 60-180 seconds)

### Datasets Queried

#### Waterways
- **Tags:** `waterway=river`, `waterway=stream`
- **Description:** Detailed river and stream networks
- **Usage:** Fine-grained hydrographic features

#### Forests
- **Tags:** `landuse=forest`, `natural=wood`
- **Description:** Forested areas and natural woodlands
- **Usage:** Showing forest cover in the watershed

#### Mountain Peaks
- **Tags:** `natural=peak`
- **Description:** Named mountain peaks with elevation data
- **Usage:** Topographic features and elevation points

### Sample Query Format
```overpass
[out:json][timeout:60];
(
  way["waterway"="river"](46.5,-124.5,50.5,-121.5);
  way["waterway"="stream"](46.5,-124.5,50.5,-121.5);
);
out geom;
```

## 3. USGS National Hydrography Dataset (NHD)

### Description
High-resolution digital spatial data representing water features across the United States.

### Access
- **Website:** https://www.usgs.gov/national-hydrography/access-national-hydrography-products
- **Format:** Geodatabase (GDB), Shapefile (SHP)
- **License:** Public Domain (US Government Work)

### Relevant HUC-8 Watersheds
- **17110019:** Puget Sound
- **17110020:** Snohomish River
- **17110018:** Duwamish-Cedar Rivers
- **17110021:** Stillaguamish River
- **17110022:** Skagit River

### Features
- Stream networks
- Watershed boundaries
- Flow direction
- Stream order classification

### Note
Due to large file sizes, NHD data is not automatically downloaded. Users should manually download relevant HUC-8 watersheds from the USGS website.

## 4. Elevation Data

### SRTM (Shuttle Radar Topography Mission)

#### Description
Near-global digital elevation model (DEM) from NASA's 2000 Space Shuttle mission.

#### Specifications
- **Resolution:** 90m (3 arc-second) or 30m (1 arc-second)
- **Coverage:** 60°N to 56°S latitude
- **Vertical Accuracy:** ±16m absolute, ±6m relative
- **Format:** GeoTIFF

#### Access
- **Website:** https://srtm.csi.cgiar.org/
- **Python Package:** `elevation` (automates downloading and processing)
- **License:** Public Domain

#### Usage
```python
import elevation
elevation.clip(bounds=(min_lon, min_lat, max_lon, max_lat), 
               output='salish_sea_dem.tif')
```

### Alternative: ASTER GDEM

#### Description
Global digital elevation model from NASA and METI Japan.

#### Specifications
- **Resolution:** 30m (1 arc-second)
- **Coverage:** 83°N to 83°S latitude
- **License:** Public Domain

## 5. Boundaries and Context

### Salish Sea Boundary
- **Custom Definition:** Bounding box defined in `config.py`
- **Coordinates:** 
  - Longitude: -124.5° to -121.5°W
  - Latitude: 46.5° to 50.5°N
- **Usage:** Defines the focus area for data clipping and visualization

## Data Processing Pipeline

1. **Download:** `download_data.py` fetches data from sources
2. **Storage:** Raw data stored in `data/raw/` (gitignored)
3. **Processing:** `process_data.py` clips, filters, and simplifies
4. **Output:** Processed GeoJSON files in `data/processed/`
5. **Visualization:** Map generation scripts read processed data

## Data Update Frequency

- **Natural Earth:** Updated periodically (check website for versions)
- **OSM:** Real-time (data is continuously updated by contributors)
- **USGS NHD:** Updated annually
- **SRTM:** Static (mission completed in 2000)

## Licensing Summary

All data sources used in this project are in the public domain or available under open licenses:

- **Natural Earth:** Public Domain
- **OpenStreetMap:** ODbL (Open Database License)
- **USGS Data:** Public Domain (US Government Work)
- **SRTM:** Public Domain

## Attribution

When using this project or its data, please provide attribution:

```
Data sources: Natural Earth, OpenStreetMap Contributors, 
USGS National Hydrography Dataset, NASA SRTM
```

## Additional Resources

- [Natural Earth Documentation](https://www.naturalearthdata.com/about/)
- [OSM Wiki](https://wiki.openstreetmap.org/)
- [USGS NHD User Guide](https://pubs.usgs.gov/tm/11/a1/)
- [SRTM Documentation](https://www2.jpl.nasa.gov/srtm/)
