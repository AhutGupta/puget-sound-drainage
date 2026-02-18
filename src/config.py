"""
Configuration for Salish Sea Drainage Map Project
"""

# Salish Sea bounding box (approximate)
# Covers Puget Sound, Georgia Strait, and surrounding areas
SALISH_SEA_BOUNDS = {
    'min_lon': -124.5,
    'max_lon': -121.5,
    'min_lat': 46.5,
    'max_lat': 50.5
}

# Data sources for open geospatial data
DATA_SOURCES = {
    # Natural Earth Data for base maps
    'natural_earth': {
        'coastlines': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_coastline.zip',
        'rivers': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_rivers_lake_centerlines.zip',
        'lakes': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_lakes.zip',
    },
    
    # USGS National Hydrography Dataset
    'usgs_nhd': {
        'info': 'https://www.usgs.gov/national-hydrography/access-national-hydrography-products',
        'note': 'Use HUC-8 watersheds: 17110019 (Puget Sound), 17110020 (Snohomish)'
    },
    
    # OpenStreetMap for detailed features
    'osm': {
        'overpass_api': 'https://overpass-api.de/api/interpreter',
        'note': 'Query for rivers, streams, forests, peaks in region'
    },
    
    # Elevation data (SRTM or ASTER GDEM)
    'elevation': {
        'srtm': 'https://srtm.csi.cgiar.org/',
        'note': 'Use elevation package to download SRTM tiles'
    }
}

# Map styling
MAP_STYLE = {
    'salish_sea_color': '#4A90E2',  # Blue for water
    'river_color': '#6FB3E0',        # Light blue for rivers
    'forest_color': '#2D5016',       # Dark green for forests
    'mountain_color': '#8B7355',     # Brown for mountains
    'grey_border': '#CCCCCC',        # Grey for surrounding areas
    'boundary_color': '#888888'      # Darker grey for boundaries
}

# Web application settings
WEB_CONFIG = {
    'title': 'Salish Sea Watershed Interactive Map',
    'center_lat': 48.0,
    'center_lon': -123.0,
    'default_zoom': 8,
    'tile_provider': 'OpenStreetMap'
}

# Processing settings
PROCESSING_CONFIG = {
    'simplify_tolerance': 0.001,  # Simplify geometries for web display
    'elevation_resolution': 90,    # meters (SRTM3)
    'contour_interval': 100        # meters
}
