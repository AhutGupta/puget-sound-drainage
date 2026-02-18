# 🌊 Salish Sea Watershed Interactive Map

A comprehensive geospatial visualization project mapping the Salish Sea watershed, including Puget Sound, Georgia Strait, and surrounding rivers, streams, mountains, and forests.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

## 🎯 Project Overview

This project creates interactive 2D and 3D maps of the Salish Sea region using open-source Python libraries and public geospatial datasets. The maps highlight the watershed area in color while greying out surrounding border areas for context.

**Live Demo:** [View Interactive Maps](https://ahutgupta.github.io/puget-sound-drainage/)

## ✨ Features

- **🗺️ Interactive 2D Map** - Explore the region with toggleable layers (coastlines, rivers, forests, peaks)
- **🏔️ 3D Terrain Visualization** - Rotate and zoom through a 3D model of the topography
- **🌊 Salish Sea Focus** - Highlighted watershed area with greyed-out borders
- **🌲 Multiple Data Layers** - Rivers, streams, forests, mountains, and coastlines
- **📊 Open Data** - All data from reliable public sources (Natural Earth, OSM, USGS)
- **🌐 GitHub Pages** - Hosted as a static website with interactive maps

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AhutGupta/puget-sound-drainage.git
   cd puget-sound-drainage
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Demo (2 minutes)

Want to see the project in action immediately? Use sample data:

```bash
# Generate sample data and maps
python src/create_sample_data.py
python src/visualize_2d.py
python src/visualize_3d.py

# Open web/index.html in your browser
```

See [QUICKSTART.md](QUICKSTART.md) for more details.

### Full Usage (Real Data)

Follow these steps to generate the maps:

1. **Download geospatial data:**
   ```bash
   python src/download_data.py
   ```
   This downloads Natural Earth data and OpenStreetMap features for the region.

2. **Process the data:**
   ```bash
   python src/process_data.py
   ```
   This clips, simplifies, and converts data to GeoJSON format.

3. **Generate 2D map:**
   ```bash
   python src/visualize_2d.py
   ```
   Creates an interactive Folium map at `web/map_2d.html`

4. **Generate 3D map:**
   ```bash
   python src/visualize_3d.py
   ```
   Creates an interactive Plotly 3D visualization at `web/map_3d.html`

5. **View the maps:**
   - Open `web/index.html` in a web browser for the landing page
   - Or directly open `web/map_2d.html` or `web/map_3d.html`

## 📁 Project Structure

```
puget-sound-drainage/
├── src/                      # Source code
│   ├── config.py            # Configuration and data sources
│   ├── download_data.py     # Download geospatial datasets
│   ├── process_data.py      # Process and prepare map data
│   ├── visualize_2d.py      # Generate 2D Folium map
│   └── visualize_3d.py      # Generate 3D Plotly map
├── data/
│   ├── raw/                 # Downloaded raw data (gitignored)
│   └── processed/           # Processed GeoJSON files (gitignored)
├── web/                     # GitHub Pages website
│   ├── index.html          # Landing page
│   ├── map_2d.html         # 2D interactive map (generated)
│   ├── map_3d.html         # 3D interactive map (generated)
│   └── assets/
│       ├── css/            # Stylesheets
│       └── js/             # JavaScript files
├── docs/                    # Additional documentation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📊 Data Sources

### Natural Earth Data
- **Coastlines:** 1:10m physical coastline vectors
- **Rivers:** 1:10m rivers and lake centerlines
- **Lakes:** 1:10m lake polygons
- **Source:** https://www.naturalearthdata.com/

### OpenStreetMap (via Overpass API)
- **Waterways:** Rivers and streams in the region
- **Forests:** Forest and woodland areas
- **Peaks:** Mountain peaks with elevations
- **Source:** https://www.openstreetmap.org/

### USGS National Hydrography Dataset
- **Watersheds:** HUC-8 watershed boundaries for Puget Sound
- **Source:** https://www.usgs.gov/national-hydrography

### Elevation Data
- **SRTM:** Shuttle Radar Topography Mission (90m resolution)
- **Source:** https://srtm.csi.cgiar.org/

## 🛠️ Technologies

- **GeoPandas** - Geospatial data manipulation
- **Shapely** - Geometric operations
- **Folium** - Interactive 2D web maps
- **Plotly** - Interactive 3D visualizations
- **Requests** - Data downloading
- **NumPy/Pandas** - Data processing

## 🌐 GitHub Pages Deployment

The project is configured for easy deployment to GitHub Pages:

1. Generate the maps (follow Usage steps above)
2. Ensure `web/` directory contains:
   - `index.html`
   - `map_2d.html`
   - `map_3d.html`
   - `assets/` folder
3. Push to GitHub
4. Enable GitHub Pages in repository settings (use `/web` folder or configure as needed)

## 🗺️ Map Layers

### 2D Map Features
- Salish Sea coastlines (blue)
- Major rivers and streams (light blue)
- Forest areas (dark green)
- Mountain peaks (brown markers)
- Grey surrounding areas for context
- Interactive tooltips and layer controls

### 3D Map Features
- Terrain elevation surface with color gradient
- Rivers as 3D lines
- Mountain peaks as 3D markers
- Rotatable, zoomable view
- Elevation colorbar and hover information

## 🎨 Color Scheme

- **Salish Sea:** #4A90E2 (Blue)
- **Rivers/Streams:** #6FB3E0 (Light Blue)
- **Forests:** #2D5016 (Dark Green)
- **Mountains:** #8B7355 (Brown)
- **Border Areas:** #CCCCCC (Grey, 30% opacity)

## 📝 Configuration

Edit `src/config.py` to customize:
- Geographic bounds of the region
- Data source URLs
- Map styling and colors
- Processing parameters
- Web application settings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Natural Earth for providing high-quality public domain map data
- OpenStreetMap contributors for detailed geographic features
- USGS for hydrography and watershed data
- The Python geospatial community for excellent tools and libraries

## 📧 Contact

**Ahut Gupta**
- GitHub: [@AhutGupta](https://github.com/AhutGupta)
- Project Link: [https://github.com/AhutGupta/puget-sound-drainage](https://github.com/AhutGupta/puget-sound-drainage)

---

**Note:** This is an educational and visualization project. For official watershed management data and analysis, please consult relevant government agencies and environmental organizations.
