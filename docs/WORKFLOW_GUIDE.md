# Workflow Guide

This guide walks through the complete workflow for creating the Salish Sea watershed maps.

## Complete Workflow

### Step 1: Setup Environment

```bash
# Clone the repository
git clone https://github.com/AhutGupta/puget-sound-drainage.git
cd puget-sound-drainage

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Data

```bash
python src/download_data.py
```

**What happens:**
- Creates `data/raw/` directory structure
- Downloads Natural Earth coastlines, rivers, and lakes
- Queries OpenStreetMap Overpass API for:
  - Waterways (rivers and streams)
  - Forests (landuse=forest, natural=wood)
  - Mountain peaks (natural=peak)
- Creates Salish Sea boundary GeoJSON

**Expected output:**
```
data/raw/
├── natural_earth/
│   ├── coastlines/
│   ├── rivers/
│   └── lakes/
├── osm/
│   ├── waterways.json
│   ├── forests.json
│   └── peaks.json
└── salish_sea_boundary.geojson
```

**Time:** 2-5 minutes (depending on network speed)

### Step 3: Process Data

```bash
python src/process_data.py
```

**What happens:**
- Loads raw shapefiles and JSON data
- Clips geometries to Salish Sea region
- Simplifies geometries for web display
- Converts all data to GeoJSON format
- Creates data summary

**Expected output:**
```
data/processed/
├── coastlines.geojson
├── rivers.geojson
├── osm_waterways.geojson
├── osm_forests.geojson
├── osm_peaks.geojson
└── summary.json
```

**Time:** 1-3 minutes

### Step 4: Generate 2D Map

```bash
python src/visualize_2d.py
```

**What happens:**
- Creates Folium map centered on Salish Sea
- Adds grey boundary for surrounding areas
- Adds data layers:
  - Coastlines (blue)
  - Rivers (light blue)
  - Forests (green)
  - Peaks (brown)
- Adds interactive controls, legend, and title
- Saves as HTML file

**Expected output:**
```
web/map_2d.html
```

**Time:** 10-30 seconds

### Step 5: Generate 3D Map

```bash
python src/visualize_3d.py
```

**What happens:**
- Creates synthetic 3D terrain grid
- Builds Plotly 3D surface plot
- Adds rivers as 3D lines
- Adds peaks as 3D markers
- Configures camera and controls
- Saves as HTML file

**Expected output:**
```
web/map_3d.html
```

**Time:** 10-30 seconds

### Step 6: View the Maps

Open the maps in your web browser:

```bash
# Option 1: Direct file opening
# Navigate to web/ directory and open files

# Option 2: Simple HTTP server
cd web
python -m http.server 8000
# Then visit http://localhost:8000 in browser
```

## Quick Start (All Steps)

Run all steps in sequence:

```bash
# From project root directory
python src/download_data.py && \
python src/process_data.py && \
python src/visualize_2d.py && \
python src/visualize_3d.py && \
echo "Maps generated! Open web/index.html in your browser."
```

## GitHub Pages Deployment

### Manual Deployment

1. Generate maps using steps above
2. Commit changes:
   ```bash
   git add web/
   git commit -m "Update maps"
   git push origin main
   ```
3. GitHub Actions will automatically deploy to Pages

### Automatic Deployment

The `.github/workflows/deploy.yml` workflow automatically deploys the `web/` directory to GitHub Pages when you push to the main branch.

To enable:
1. Go to repository Settings
2. Navigate to Pages section
3. Set Source to "GitHub Actions"
4. The site will be available at: `https://[username].github.io/[repo-name]/`

## Customization Workflow

### Changing the Region

1. Edit `src/config.py`:
   ```python
   SALISH_SEA_BOUNDS = {
       'min_lon': -125.0,
       'max_lon': -120.0,
       'min_lat': 45.0,
       'max_lat': 51.0
   }
   ```

2. Re-run download and processing:
   ```bash
   rm -rf data/raw/* data/processed/*
   python src/download_data.py
   python src/process_data.py
   ```

3. Regenerate maps:
   ```bash
   python src/visualize_2d.py
   python src/visualize_3d.py
   ```

### Adding Custom Data

1. Add data source to `src/config.py`
2. Create download function in `src/download_data.py`
3. Create processing function in `src/process_data.py`
4. Add layer to visualization scripts
5. Run workflow

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed instructions.

## Troubleshooting

### Data Download Issues

**Problem:** Natural Earth download fails
```
Solution: Check internet connection, try again later
```

**Problem:** Overpass API timeout
```
Solution: 
- Reduce query area in config.py
- Increase timeout in download_data.py
- Try during off-peak hours
```

### Processing Issues

**Problem:** No data in processed files
```
Solution:
- Verify raw data was downloaded successfully
- Check that bounds in config.py are correct
- Ensure region has data coverage
```

**Problem:** Memory error
```
Solution:
- Increase simplify_tolerance in config.py
- Process one layer at a time
- Use a machine with more RAM
```

### Visualization Issues

**Problem:** Map doesn't render
```
Solution:
- Check browser console for errors
- Verify processed data exists
- Try opening in different browser
```

**Problem:** Map is empty
```
Solution:
- Verify data was clipped correctly
- Check coordinate systems (should be EPSG:4326)
- Inspect processed GeoJSON files
```

## Best Practices

1. **Always use virtual environment** to avoid dependency conflicts
2. **Run scripts from project root** for correct relative paths
3. **Check data quality** after each step
4. **Keep raw data** in case you need to reprocess
5. **Version control** your configuration changes
6. **Test locally** before deploying to GitHub Pages

## Performance Tips

### For Faster Processing

- Use lower resolution Natural Earth data (50m instead of 10m)
- Increase simplify_tolerance for smaller files
- Filter out less important features
- Process data in parallel (advanced)

### For Smaller Web Files

- Aggressive geometry simplification
- Remove unnecessary attributes from GeoJSON
- Compress files before deployment
- Use vector tiles for very large datasets

## Advanced Workflows

### Jupyter Notebook Exploration

```bash
# Install Jupyter
pip install jupyter

# Start notebook
jupyter notebook

# Create new notebook and explore data interactively
```

### Automated Updates

Set up a cron job or GitHub Actions workflow to:
1. Download fresh OSM data weekly
2. Reprocess automatically
3. Deploy updated maps

### Custom Analysis

Use the processed GeoJSON data for:
- Watershed analysis
- Flow direction modeling
- Habitat connectivity
- Climate impact assessment

## Next Steps

After completing the basic workflow:

1. **Explore the data** - Open GeoJSON files in QGIS or geojson.io
2. **Customize styling** - Modify colors and display options
3. **Add more layers** - Include roads, cities, protected areas
4. **Improve 3D terrain** - Download real SRTM elevation data
5. **Share your maps** - Deploy to GitHub Pages and share the link!

## Resources

- [Project README](../README.md)
- [Data Sources Documentation](DATA_SOURCES.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [GitHub Pages Documentation](https://pages.github.com/)
