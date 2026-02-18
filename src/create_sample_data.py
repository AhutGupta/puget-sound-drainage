"""
Create sample demonstration data for testing without downloading
"""

import json
from pathlib import Path
import sys
import os

# Import config
sys.path.insert(0, os.path.dirname(__file__))
from config import SALISH_SEA_BOUNDS

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def create_sample_coastlines():
    """Create sample coastline data"""
    bounds = SALISH_SEA_BOUNDS
    
    # Create a simple polygon for Puget Sound
    coastline_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Puget Sound"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-123.5, 47.0],
                        [-123.0, 47.5],
                        [-122.5, 48.0],
                        [-122.3, 48.3],
                        [-122.5, 48.5],
                        [-123.0, 48.8],
                        [-123.5, 48.5],
                        [-124.0, 48.0],
                        [-124.0, 47.5],
                        [-123.5, 47.0]
                    ]
                }
            }
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'coastlines.geojson'
    with open(output_file, 'w') as f:
        json.dump(coastline_geojson, f)
    print(f"Created: {output_file}")


def create_sample_rivers():
    """Create sample river data"""
    rivers_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Skagit River"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-121.5, 48.5],
                        [-122.0, 48.4],
                        [-122.3, 48.3]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Snohomish River"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-121.8, 47.9],
                        [-122.1, 47.9],
                        [-122.2, 47.95]
                    ]
                }
            }
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'rivers.geojson'
    with open(output_file, 'w') as f:
        json.dump(rivers_geojson, f)
    print(f"Created: {output_file}")


def create_sample_waterways():
    """Create sample waterway data"""
    waterways_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Sample Creek", "waterway": "stream"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-122.5, 47.5],
                        [-122.6, 47.6]
                    ]
                }
            }
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'osm_waterways.geojson'
    with open(output_file, 'w') as f:
        json.dump(waterways_geojson, f)
    print(f"Created: {output_file}")


def create_sample_forests():
    """Create sample forest data"""
    forests_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Olympic National Forest", "type": "forest"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-123.8, 47.8],
                        [-123.5, 47.8],
                        [-123.5, 48.1],
                        [-123.8, 48.1],
                        [-123.8, 47.8]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Mount Baker-Snoqualmie", "type": "forest"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-122.0, 48.3],
                        [-121.7, 48.3],
                        [-121.7, 48.6],
                        [-122.0, 48.6],
                        [-122.0, 48.3]
                    ]]
                }
            }
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'osm_forests.geojson'
    with open(output_file, 'w') as f:
        json.dump(forests_geojson, f)
    print(f"Created: {output_file}")


def create_sample_peaks():
    """Create sample mountain peak data"""
    peaks_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Mount Baker", "elevation": "3286"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-121.81, 48.78]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Mount Rainier", "elevation": "4392"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-121.76, 46.85]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Mount Olympus", "elevation": "2428"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-123.71, 47.80]
                }
            }
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'osm_peaks.geojson'
    with open(output_file, 'w') as f:
        json.dump(peaks_geojson, f)
    print(f"Created: {output_file}")


def create_summary():
    """Create data summary"""
    summary = {
        "region": "Salish Sea (Sample Data)",
        "bounds": SALISH_SEA_BOUNDS,
        "processed_layers": [
            {"name": "coastlines", "features": 1, "file": "coastlines.geojson"},
            {"name": "rivers", "features": 2, "file": "rivers.geojson"},
            {"name": "osm_waterways", "features": 1, "file": "osm_waterways.geojson"},
            {"name": "osm_forests", "features": 2, "file": "osm_forests.geojson"},
            {"name": "osm_peaks", "features": 3, "file": "osm_peaks.geojson"}
        ]
    }
    
    output_file = DATA_PROCESSED_DIR / 'summary.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Created: {output_file}")


def main():
    """Create all sample data"""
    print("=" * 60)
    print("Creating Sample Data for Demonstration")
    print("=" * 60)
    print("\nThis creates minimal sample data to demonstrate the")
    print("visualization workflow without downloading real datasets.\n")
    
    create_sample_coastlines()
    create_sample_rivers()
    create_sample_waterways()
    create_sample_forests()
    create_sample_peaks()
    create_summary()
    
    print("\n" + "=" * 60)
    print("Sample Data Created Successfully!")
    print("=" * 60)
    print(f"\nFiles created in: {DATA_PROCESSED_DIR}")
    print("\nNow you can run:")
    print("  python src/visualize_2d.py")
    print("  python src/visualize_3d.py")


if __name__ == '__main__':
    main()
