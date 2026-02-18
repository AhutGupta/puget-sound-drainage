"""
Configuration for Salish Sea Drainage Map Project
"""

# Expanded Salish Sea bounding box
# Covers Puget Sound, Georgia Strait, Cascade Range, and Olympic Mountains
# Expanded to include all major stream sources from mountains to sea
SALISH_SEA_BOUNDS = {
    'min_lon': -125.5,  # Extended west to cover Olympic Peninsula fully
    'max_lon': -120.0,  # Extended east to cover Cascade Range
    'min_lat': 45.5,    # Extended south to cover southern Cascades watersheds
    'max_lat': 51.0     # Extended north to cover Canadian watersheds
}

# Data sources for open geospatial data
DATA_SOURCES = {
    # Natural Earth Data for base maps
    'natural_earth': {
        'coastlines': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_coastline.zip',
        'rivers': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_rivers_lake_centerlines.zip',
        'lakes': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_lakes.zip',
        'populated_places': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_populated_places.zip',
    },
    
    # USGS National Hydrography Dataset
    'usgs_nhd': {
        'info': 'https://www.usgs.gov/national-hydrography/access-national-hydrography-products',
        'note': 'Use HUC-8 watersheds: 17110019 (Puget Sound), 17110020 (Snohomish)'
    },
    
    # OpenStreetMap for detailed features
    'osm': {
        'overpass_api': 'https://overpass-api.de/api/interpreter',
        'note': 'Query for rivers, streams, forests, peaks, and populated places in region'
    },
    
    # Elevation data (SRTM or ASTER GDEM)
    'elevation': {
        'srtm': 'https://srtm.csi.cgiar.org/',
        'note': 'Use elevation package to download SRTM tiles'
    }
}

# Population center settings
POPULATION_CONFIG = {
    'min_population': 10000,  # Minimum population to display
    'label_places': True,      # Whether to add labels to populated places
    'include_us': True,        # Include US cities
    'include_canada': True     # Include Canadian cities
}

# Map styling
MAP_STYLE = {
    'salish_sea_color': '#4A90E2',  # Blue for water
    'river_color': '#6FB3E0',        # Light blue for rivers
    'forest_color': '#2D5016',       # Dark green for forests
    'mountain_color': '#8B7355',     # Brown for mountains
    'grey_border': '#CCCCCC',        # Grey for surrounding areas
    'boundary_color': '#888888',     # Darker grey for boundaries
    'city_color': '#FF6B6B'          # Red for populated places
}

# Web application settings
WEB_CONFIG = {
    'title': 'Salish Sea Watershed Interactive Map',
    'center_lat': 48.0,
    'center_lon': -123.0,
    'default_zoom': 7,  # Adjusted for larger area
    'tile_provider': 'OpenStreetMap'
}

# Processing settings
PROCESSING_CONFIG = {
    'simplify_tolerance': 0.001,  # Simplify geometries for web display
    'elevation_resolution': 90,    # meters (SRTM3)
    'contour_interval': 100        # meters
}