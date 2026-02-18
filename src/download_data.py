"""
Download geospatial data for Salish Sea region
"""

import os
import requests
import zipfile
from pathlib import Path
import json

# Import config
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import SALISH_SEA_BOUNDS, DATA_SOURCES

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / 'data' / 'raw'
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_file(url, dest_path):
    """Download a file from URL to destination path"""
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  -> Saved to {dest_path}")
        return True
    except Exception as e:
        print(f"  -> Error: {e}")
        return False


def extract_zip(zip_path, extract_dir):
    """Extract a zip file"""
    print(f"Extracting {zip_path.name}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"  -> Extracted to {extract_dir}")
        return True
    except Exception as e:
        print(f"  -> Error: {e}")
        return False


def download_natural_earth_data():
    """Download Natural Earth datasets"""
    print("\n=== Downloading Natural Earth Data ===")
    
    ne_dir = DATA_RAW_DIR / 'natural_earth'
    ne_dir.mkdir(exist_ok=True)
    
    for name, url in DATA_SOURCES['natural_earth'].items():
        zip_path = ne_dir / f"{name}.zip"
        
        if not zip_path.exists():
            if download_file(url, zip_path):
                extract_dir = ne_dir / name
                extract_dir.mkdir(exist_ok=True)
                extract_zip(zip_path, extract_dir)
        else:
            print(f"  -> {name} already downloaded")


def download_osm_data():
    """Download OpenStreetMap data using Overpass API"""
    print("\n=== Downloading OpenStreetMap Data ===")
    
    osm_dir = DATA_RAW_DIR / 'osm'
    osm_dir.mkdir(exist_ok=True)
    
    bounds = SALISH_SEA_BOUNDS
    bbox = f"{bounds['min_lat']},{bounds['min_lon']},{bounds['max_lat']},{bounds['max_lon']}"
    
    # Query for rivers and streams
    queries = {
        'waterways': f"""
        [out:json][timeout:60];
        (
          way["waterway"="river"]({bbox});
          way["waterway"="stream"]({bbox});
        );
        out geom;
        """,
        'forests': f"""
        [out:json][timeout:60];
        (
          way["landuse"="forest"]({bbox});
          way["natural"="wood"]({bbox});
        );
        out geom;
        """,
        'peaks': f"""
        [out:json][timeout:60];
        (
          node["natural"="peak"]({bbox});
        );
        out;
        """
    }
    
    overpass_url = DATA_SOURCES['osm']['overpass_api']
    
    for name, query in queries.items():
        output_file = osm_dir / f"{name}.json"
        
        if not output_file.exists():
            print(f"Querying OSM for {name}...")
            try:
                response = requests.post(overpass_url, data=query, timeout=90)
                response.raise_for_status()
                
                with open(output_file, 'w') as f:
                    json.dump(response.json(), f, indent=2)
                
                print(f"  -> Saved to {output_file}")
            except Exception as e:
                print(f"  -> Error: {e}")
        else:
            print(f"  -> {name} already downloaded")


def create_salish_sea_boundary():
    """Create a GeoJSON for the Salish Sea focus area"""
    print("\n=== Creating Salish Sea Boundary ===")
    
    bounds = SALISH_SEA_BOUNDS
    
    # Create a polygon for the region
    boundary = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "name": "Salish Sea Region",
                "description": "Puget Sound and Georgia Strait watershed"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [bounds['min_lon'], bounds['min_lat']],
                    [bounds['max_lon'], bounds['min_lat']],
                    [bounds['max_lon'], bounds['max_lat']],
                    [bounds['min_lon'], bounds['max_lat']],
                    [bounds['min_lon'], bounds['min_lat']]
                ]]
            }
        }]
    }
    
    boundary_file = DATA_RAW_DIR / 'salish_sea_boundary.geojson'
    with open(boundary_file, 'w') as f:
        json.dump(boundary, f, indent=2)
    
    print(f"  -> Created boundary file: {boundary_file}")


def main():
    """Main download function"""
    print("=" * 60)
    print("Salish Sea Data Download Script")
    print("=" * 60)
    
    # Create boundary file
    create_salish_sea_boundary()
    
    # Download Natural Earth data
    download_natural_earth_data()
    
    # Download OSM data
    download_osm_data()
    
    print("\n" + "=" * 60)
    print("Download Complete!")
    print("=" * 60)
    print("\nNote: For elevation data, run process_data.py which will")
    print("automatically download SRTM tiles for the region.")
    print("\nFor USGS NHD data, visit:")
    print("  https://www.usgs.gov/national-hydrography/access-national-hydrography-products")
    print("  and download HUC-8 watersheets for Puget Sound region")


if __name__ == '__main__':
    main()
