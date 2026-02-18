"""
Process downloaded geospatial data for Salish Sea visualization
"""

import os
import json
from pathlib import Path
import geopandas as gpd
from shapely.geometry import shape, Point, LineString, Polygon
import pandas as pd

# Import config
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import SALISH_SEA_BOUNDS, PROCESSING_CONFIG

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / 'data' / 'raw'
DATA_PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_salish_sea_boundary():
    """Load the Salish Sea boundary"""
    boundary_file = DATA_RAW_DIR / 'salish_sea_boundary.geojson'
    return gpd.read_file(boundary_file)


def process_natural_earth_coastlines():
    """Process Natural Earth coastline data"""
    print("\n=== Processing Coastlines ===")
    
    try:
        # Find coastline shapefile
        coastline_dir = DATA_RAW_DIR / 'natural_earth' / 'coastlines'
        shp_files = list(coastline_dir.glob("*.shp"))
        
        if not shp_files:
            print("  -> No coastline shapefiles found")
            return None
        
        # Load and clip to region
        gdf = gpd.read_file(shp_files[0])
        bounds = SALISH_SEA_BOUNDS
        region_box = Polygon([
            (bounds['min_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['max_lat']),
            (bounds['min_lon'], bounds['max_lat']),
            (bounds['min_lon'], bounds['min_lat'])
        ])
        
        gdf = gdf[gdf.geometry.intersects(region_box)]
        
        # Simplify for web display
        gdf['geometry'] = gdf['geometry'].simplify(PROCESSING_CONFIG['simplify_tolerance'])
        
        # Save processed data
        output_file = DATA_PROCESSED_DIR / 'coastlines.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} coastline features")
        print(f"  -> Saved to {output_file}")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None


def process_natural_earth_rivers():
    """Process Natural Earth river data"""
    print("\n=== Processing Rivers ===")
    
    try:
        # Find rivers shapefile
        rivers_dir = DATA_RAW_DIR / 'natural_earth' / 'rivers'
        shp_files = list(rivers_dir.glob("*.shp"))
        
        if not shp_files:
            print("  -> No river shapefiles found")
            return None
        
        # Load and clip to region
        gdf = gpd.read_file(shp_files[0])
        bounds = SALISH_SEA_BOUNDS
        region_box = Polygon([
            (bounds['min_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['max_lat']),
            (bounds['min_lon'], bounds['max_lat']),
            (bounds['min_lon'], bounds['min_lat'])
        ])
        
        gdf = gdf[gdf.geometry.intersects(region_box)]
        
        # Simplify for web display
        gdf['geometry'] = gdf['geometry'].simplify(PROCESSING_CONFIG['simplify_tolerance'])
        
        # Save processed data
        output_file = DATA_PROCESSED_DIR / 'rivers.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} river features")
        print(f"  -> Saved to {output_file}")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None


def process_osm_waterways():
    """Process OSM waterway data"""
    print("\n=== Processing OSM Waterways ===")
    
    try:
        waterways_file = DATA_RAW_DIR / 'osm' / 'waterways.json'
        
        if not waterways_file.exists():
            print("  -> OSM waterways file not found")
            return None
        
        # Load OSM JSON
        with open(waterways_file, 'r') as f:
            data = json.load(f)
        
        # Convert to GeoDataFrame
        features = []
        for element in data.get('elements', []):
            if 'geometry' in element:
                coords = [(node['lon'], node['lat']) for node in element['geometry']]
                if len(coords) >= 2:
                    geom = LineString(coords)
                    features.append({
                        'geometry': geom,
                        'name': element.get('tags', {}).get('name', 'Unnamed'),
                        'waterway': element.get('tags', {}).get('waterway', 'unknown')
                    })
        
        if not features:
            print("  -> No waterway features found")
            return None
        
        gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
        
        # Simplify for web display
        gdf['geometry'] = gdf['geometry'].simplify(PROCESSING_CONFIG['simplify_tolerance'])
        
        # Save processed data
        output_file = DATA_PROCESSED_DIR / 'osm_waterways.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} waterway features")
        print(f"  -> Saved to {output_file}")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None


def process_osm_forests():
    """Process OSM forest data"""
    print("\n=== Processing OSM Forests ===")
    
    try:
        forests_file = DATA_RAW_DIR / 'osm' / 'forests.json'
        
        if not forests_file.exists():
            print("  -> OSM forests file not found")
            return None
        
        # Load OSM JSON
        with open(forests_file, 'r') as f:
            data = json.load(f)
        
        # Convert to GeoDataFrame
        features = []
        for element in data.get('elements', []):
            if 'geometry' in element:
                coords = [(node['lon'], node['lat']) for node in element['geometry']]
                if len(coords) >= 3:
                    geom = Polygon(coords)
                    features.append({
                        'geometry': geom,
                        'name': element.get('tags', {}).get('name', 'Forest'),
                        'type': element.get('tags', {}).get('landuse', element.get('tags', {}).get('natural', 'forest'))
                    })
        
        if not features:
            print("  -> No forest features found")
            return None
        
        gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
        
        # Simplify for web display
        gdf['geometry'] = gdf['geometry'].simplify(PROCESSING_CONFIG['simplify_tolerance'])
        
        # Save processed data
        output_file = DATA_PROCESSED_DIR / 'osm_forests.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} forest features")
        print(f"  -> Saved to {output_file}")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None


def process_osm_peaks():
    """Process OSM mountain peak data"""
    print("\n=== Processing OSM Peaks ===")
    
    try:
        peaks_file = DATA_RAW_DIR / 'osm' / 'peaks.json'
        
        if not peaks_file.exists():
            print("  -> OSM peaks file not found")
            return None
        
        # Load OSM JSON
        with open(peaks_file, 'r') as f:
            data = json.load(f)
        
        # Convert to GeoDataFrame
        features = []
        for element in data.get('elements', []):
            if 'lat' in element and 'lon' in element:
                geom = Point(element['lon'], element['lat'])
                features.append({
                    'geometry': geom,
                    'name': element.get('tags', {}).get('name', 'Unnamed Peak'),
                    'elevation': element.get('tags', {}).get('ele', None)
                })
        
        if not features:
            print("  -> No peak features found")
            return None
        
        gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
        
        # Save processed data
        output_file = DATA_PROCESSED_DIR / 'osm_peaks.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} peak features")
        print(f"  -> Saved to {output_file}")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None


def create_summary():
    """Create a summary of processed data"""
    print("\n=== Creating Data Summary ===")
    
    summary = {
        'region': 'Salish Sea',
        'bounds': SALISH_SEA_BOUNDS,
        'processed_layers': []
    }
    
    # Check for processed files
    for file in DATA_PROCESSED_DIR.glob('*.geojson'):
        try:
            gdf = gpd.read_file(file)
            summary['processed_layers'].append({
                'name': file.stem,
                'features': len(gdf),
                'file': file.name
            })
        except:
            pass
    
    # Save summary
    summary_file = DATA_PROCESSED_DIR / 'summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"  -> Created summary: {summary_file}")
    print(f"  -> Processed {len(summary['processed_layers'])} layers")
    
    return summary


def main():
    """Main processing function"""
    print("=" * 60)
    print("Salish Sea Data Processing Script")
    print("=" * 60)
    
    # Process Natural Earth data
    process_natural_earth_coastlines()
    process_natural_earth_rivers()
    
    # Process OSM data
    process_osm_waterways()
    process_osm_forests()
    process_osm_peaks()
    
    # Create summary
    summary = create_summary()
    
    print("\n" + "=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print(f"\nProcessed {len(summary['processed_layers'])} layers")
    print(f"Output directory: {DATA_PROCESSED_DIR}")


if __name__ == '__main__':
    main()
