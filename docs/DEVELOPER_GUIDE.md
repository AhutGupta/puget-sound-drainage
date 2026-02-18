# Developer Guide

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Text editor or IDE (VS Code, PyCharm, etc.)

### Environment Setup

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development tools (optional):**
   ```bash
   pip install jupyter notebook ipython black flake8
   ```

## Project Architecture

### Core Modules

#### `src/config.py`
Central configuration file containing:
- Geographic boundaries
- Data source URLs
- Styling parameters
- Processing settings

**Key Variables:**
```python
SALISH_SEA_BOUNDS = {
    'min_lon': -125.5,  # Extended west to cover Olympic Peninsula
    'max_lon': -120.0,  # Extended east to cover Cascade Range
    'min_lat': 45.5,    # Extended south to cover southern watersheds
    'max_lat': 51.0     # Extended north to cover Canadian watersheds
}
```

#### `src/download_data.py`
Downloads raw geospatial data from various sources.

**Key Functions:**
- `download_file(url, dest_path)` - Downloads a file with error handling
- `download_natural_earth_data()` - Fetches Natural Earth datasets
- `download_osm_data()` - Queries Overpass API for OSM features
- `create_salish_sea_boundary()` - Generates the focus area boundary

**Usage:**
```bash
python src/download_data.py
```

#### `src/process_data.py`
Processes raw data into web-ready GeoJSON format.

**Key Functions:**
- `process_natural_earth_coastlines()` - Clips and simplifies coastlines
- `process_osm_waterways()` - Converts OSM JSON to GeoDataFrame
- `create_summary()` - Generates metadata about processed layers

**Processing Steps:**
1. Load raw data (Shapefiles, JSON)
2. Clip to region of interest
3. Simplify geometries for web performance
4. Convert to GeoJSON
5. Save to `data/processed/`

#### `src/visualize_2d.py`
Creates interactive 2D map using Folium.

**Key Functions:**
- `create_base_map()` - Initializes Folium map
- `add_geojson_layer()` - Adds vector layers
- `add_boundary_layer()` - Creates grey border effect
- `add_title_and_legend()` - Adds map decorations

**Output:** `web/map_2d.html`

#### `src/visualize_3d.py`
Creates 3D terrain visualization using Plotly.

**Key Functions:**
- `create_3d_terrain_base()` - Generates synthetic elevation grid
- `create_3d_map()` - Builds complete 3D scene

**Output:** `web/map_3d.html`

## Data Flow

```
Raw Data Sources (Internet)
    ↓
download_data.py
    ↓
data/raw/ (Shapefiles, JSON)
    ↓
process_data.py
    ↓
data/processed/ (GeoJSON)
    ↓
visualize_2d.py / visualize_3d.py
    ↓
web/ (HTML maps)
```

## Adding New Data Layers

### Step 1: Add Data Source to Config

Edit `src/config.py`:
```python
DATA_SOURCES = {
    'my_new_source': {
        'url': 'https://example.com/data.zip',
        'description': 'Description of data'
    }
}
```

### Step 2: Download Function

Add to `src/download_data.py`:
```python
def download_my_new_data():
    """Download my new dataset"""
    print("\n=== Downloading My New Data ===")
    
    # Download logic here
    dest_dir = DATA_RAW_DIR / 'my_new_data'
    dest_dir.mkdir(exist_ok=True)
    
    # ... download and extract ...
```

### Step 3: Processing Function

Add to `src/process_data.py`:
```python
def process_my_new_data():
    """Process my new dataset"""
    print("\n=== Processing My New Data ===")
    
    try:
        # Load data
        gdf = gpd.read_file(DATA_RAW_DIR / 'my_new_data' / 'file.shp')
        
        # Clip to region
        bounds = SALISH_SEA_BOUNDS
        # ... clipping logic ...
        
        # Simplify
        gdf['geometry'] = gdf['geometry'].simplify(
            PROCESSING_CONFIG['simplify_tolerance']
        )
        
        # Save
        output_file = DATA_PROCESSED_DIR / 'my_new_data.geojson'
        gdf.to_file(output_file, driver='GeoJSON')
        
        print(f"  -> Processed {len(gdf)} features")
        return gdf
        
    except Exception as e:
        print(f"  -> Error: {e}")
        return None
```

### Step 4: Visualization

Add to `src/visualize_2d.py`:
```python
# In create_2d_map() function:
add_geojson_layer(
    m, 
    'my_new_data.geojson', 
    'My New Layer', 
    '#FF6347'  # Color
)
```

## Customization

### Changing the Region

Edit `src/config.py`:
```python
SALISH_SEA_BOUNDS = {
    'min_lon': -125.0,  # Adjust these
    'max_lon': -121.0,
    'min_lat': 46.0,
    'max_lat': 51.0
}
```

### Changing Colors

Edit `src/config.py`:
```python
MAP_STYLE = {
    'salish_sea_color': '#1E90FF',  # Change to any hex color
    'forest_color': '#228B22',
    # ...
}
```

### Adjusting Simplification

More detail = larger file size:
```python
PROCESSING_CONFIG = {
    'simplify_tolerance': 0.0001,  # Smaller = more detail
}
```

## Testing

### Manual Testing

1. **Test data download:**
   ```bash
   python src/download_data.py
   ls data/raw/  # Check files were created
   ```

2. **Test data processing:**
   ```bash
   python src/process_data.py
   ls data/processed/  # Check GeoJSON files
   ```

3. **Test visualization:**
   ```bash
   python src/visualize_2d.py
   python src/visualize_3d.py
   # Open generated HTML files in browser
   ```

### Debugging Tips

**Issue:** Data not downloading
- Check internet connection
- Verify URLs in `config.py`
- Check API rate limits (especially Overpass)

**Issue:** Processing errors
- Ensure raw data was downloaded successfully
- Check coordinate reference systems match (EPSG:4326)
- Verify shapefile components (.shp, .shx, .dbf, .prj)

**Issue:** Maps not rendering
- Check browser console for JavaScript errors
- Verify GeoJSON files are valid (use geojson.io)
- Ensure file paths are correct

## Performance Optimization

### Large Datasets

For better performance with large datasets:

1. **Increase simplification tolerance:**
   ```python
   simplify_tolerance = 0.01  # More aggressive simplification
   ```

2. **Filter features by importance:**
   ```python
   # Only include major rivers
   gdf = gdf[gdf['importance'] > 5]
   ```

3. **Use lower resolution data:**
   - Natural Earth has 10m, 50m, and 110m scales
   - Use 50m for faster loading

### Web Optimization

- Keep GeoJSON files under 5MB for web
- Use vector tiles for very large datasets
- Consider server-side rendering for complex maps

## Code Style

Follow PEP 8 Python style guide:

```bash
# Format code
black src/*.py

# Check style
flake8 src/*.py
```

## Git Workflow

1. **Create feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

3. **Push and create PR:**
   ```bash
   git push origin feature/my-feature
   ```

## Troubleshooting

### Common Issues

**ImportError: No module named 'geopandas'**
- Solution: `pip install -r requirements.txt`

**OSError: [Errno 2] No such file or directory**
- Solution: Run scripts from project root directory
- Or use absolute paths

**Memory Error when processing large files**
- Solution: Process data in chunks
- Or increase system RAM/swap

**Overpass API timeout**
- Solution: Reduce query area or increase timeout
- Or query different features separately

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Resources

- [GeoPandas Documentation](https://geopandas.org/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Plotly Documentation](https://plotly.com/python/)
- [Shapely Manual](https://shapely.readthedocs.io/)
