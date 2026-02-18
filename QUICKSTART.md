# Quick Start Guide

Get started with the Salish Sea Watershed Map in just a few minutes!

## Option 1: Demo with Sample Data (Fastest - 2 minutes)

Perfect for testing the project or seeing how it works without downloading large datasets.

```bash
# 1. Clone and setup
git clone https://github.com/AhutGupta/puget-sound-drainage.git
cd puget-sound-drainage
pip install -r requirements.txt

# 2. Create sample data
python src/create_sample_data.py

# 3. Generate maps
python src/visualize_2d.py
python src/visualize_3d.py

# 4. View maps
# Open web/index.html in your browser
```

## Option 2: Full Workflow with Real Data (10-20 minutes)

Download and process real geospatial data for the complete experience.

```bash
# 1. Clone and setup
git clone https://github.com/AhutGupta/puget-sound-drainage.git
cd puget-sound-drainage
pip install -r requirements.txt

# 2. Download real geospatial data
python src/download_data.py
# This takes 2-5 minutes depending on your internet connection

# 3. Process the data
python src/process_data.py
# This takes 1-3 minutes

# 4. Generate maps
python src/visualize_2d.py
python src/visualize_3d.py

# 5. View maps
# Open web/index.html in your browser
```

## What You Get

### 🗺️ 2D Interactive Map (web/map_2d.html)
- Zoomable and pannable
- Toggle layers on/off
- Click features for information
- Legend and controls
- Optimized for web viewing

### 🏔️ 3D Terrain Visualization (web/map_3d.html)
- Rotate, zoom, and pan
- 3D elevation surface
- Interactive tooltips
- Color-coded by elevation
- Smooth controls

### 🌐 Landing Page (web/index.html)
- Project overview
- Links to both maps
- Technical documentation
- Usage instructions

## Viewing the Maps Locally

### Simple Method
Just double-click `web/index.html` to open in your default browser.

### With Local Server (Recommended)
```bash
cd web
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

## Troubleshooting

### Installation Issues

**Problem:** `pip install` fails
```bash
# Solution: Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**Problem:** Permission denied errors
```bash
# Solution: Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Runtime Issues

**Problem:** Import errors
```bash
# Solution: Make sure you're in the project root directory
cd puget-sound-drainage
python src/visualize_2d.py
```

**Problem:** Maps appear empty
```bash
# Solution: Generate sample data first
python src/create_sample_data.py
python src/visualize_2d.py
```

## Next Steps

After getting started:

1. **Explore the maps** - Try all the interactive features
2. **Customize colors** - Edit `src/config.py` to change styling
3. **Change the region** - Modify bounds in `src/config.py`
4. **Deploy to web** - Use GitHub Pages (see README)
5. **Read the docs** - Check `docs/` folder for detailed guides

## System Requirements

- Python 3.8 or higher
- 500MB disk space (for dependencies)
- 1GB RAM minimum
- Internet connection (for downloading data)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Getting Help

- **Documentation:** Check the `docs/` folder
- **Issues:** https://github.com/AhutGupta/puget-sound-drainage/issues
- **README:** Full project details in main README.md

## Quick Commands Reference

```bash
# Create sample data (fast demo)
python src/create_sample_data.py

# Download real data
python src/download_data.py

# Process data
python src/process_data.py

# Generate 2D map
python src/visualize_2d.py

# Generate 3D map
python src/visualize_3d.py

# All at once (with sample data)
python src/create_sample_data.py && \
python src/visualize_2d.py && \
python src/visualize_3d.py
```

Happy mapping! 🗺️🌊🏔️
