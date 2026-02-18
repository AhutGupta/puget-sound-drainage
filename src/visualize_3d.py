"""
Create 3D interactive map of Salish Sea region using Plotly
"""

import os
from pathlib import Path
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json

# Import config
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import SALISH_SEA_BOUNDS, MAP_STYLE, WEB_CONFIG

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
WEB_DIR = BASE_DIR / 'web'
WEB_DIR.mkdir(exist_ok=True)


def load_layer(filename):
    """Load a processed GeoJSON layer"""
    filepath = DATA_PROCESSED_DIR / filename
    if filepath.exists():
        try:
            return gpd.read_file(filepath)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return None


def create_3d_terrain_base():
    """Create a simple 3D terrain base using synthetic elevation"""
    print("Creating 3D terrain base...")
    
    bounds = SALISH_SEA_BOUNDS
    
    # Create grid
    lon_range = np.linspace(bounds['min_lon'], bounds['max_lon'], 100)
    lat_range = np.linspace(bounds['min_lat'], bounds['max_lat'], 100)
    lon_grid, lat_grid = np.meshgrid(lon_range, lat_range)
    
    # Create synthetic elevation (mountains around edges, low in center for water)
    center_lon = (bounds['min_lon'] + bounds['max_lon']) / 2
    center_lat = (bounds['min_lat'] + bounds['max_lat']) / 2
    
    # Distance from center (normalized)
    dist = np.sqrt((lon_grid - center_lon)**2 + (lat_grid - center_lat)**2)
    max_dist = np.max(dist)
    
    # Create elevation: higher at edges (mountains), lower at center (sea level)
    elevation = 2000 * (dist / max_dist) ** 2
    
    # Add some variation for visual interest
    elevation += 200 * np.sin(lon_grid * 5) * np.cos(lat_grid * 5)
    
    print(f"  -> Created {lon_grid.shape} terrain grid")
    
    return lon_grid, lat_grid, elevation


def create_3d_map():
    """Create the complete 3D map using Plotly"""
    print("=" * 60)
    print("Creating 3D Salish Sea Map")
    print("=" * 60)
    
    # Create figure
    fig = go.Figure()
    
    # Create terrain base
    lon_grid, lat_grid, elevation = create_3d_terrain_base()
    
    # Add terrain surface
    fig.add_trace(go.Surface(
        x=lon_grid,
        y=lat_grid,
        z=elevation,
        colorscale=[
            [0, MAP_STYLE['salish_sea_color']],    # Sea level - blue
            [0.3, MAP_STYLE['forest_color']],       # Low elevation - green
            [0.7, MAP_STYLE['mountain_color']],     # Mid elevation - brown
            [1, '#FFFFFF']                          # High elevation - white (snow)
        ],
        opacity=0.9,
        name='Terrain',
        showscale=True,
        colorbar=dict(
            title="Elevation (m)",
            x=1.02
        ),
        hovertemplate='Lon: %{x:.2f}<br>Lat: %{y:.2f}<br>Elevation: %{z:.0f}m<extra></extra>'
    ))
    
    # Try to add rivers as lines
    print("Adding rivers to 3D map...")
    rivers_gdf = load_layer('rivers.geojson')
    if rivers_gdf is not None and len(rivers_gdf) > 0:
        for idx, row in rivers_gdf.iterrows():
            if row.geometry.geom_type == 'LineString':
                coords = list(row.geometry.coords)
                lons = [c[0] for c in coords]
                lats = [c[1] for c in coords]
                # Rivers at elevation 10m
                elevs = [10] * len(lons)
                
                fig.add_trace(go.Scatter3d(
                    x=lons,
                    y=lats,
                    z=elevs,
                    mode='lines',
                    line=dict(color=MAP_STYLE['river_color'], width=3),
                    name='Rivers',
                    showlegend=(idx == 0),
                    hovertemplate='River<extra></extra>'
                ))
        print(f"  -> Added {len(rivers_gdf)} rivers")
    
    # Try to add peaks as points
    print("Adding peaks to 3D map...")
    peaks_gdf = load_layer('osm_peaks.geojson')
    if peaks_gdf is not None and len(peaks_gdf) > 0:
        lons = [p.x for p in peaks_gdf.geometry]
        lats = [p.y for p in peaks_gdf.geometry]
        # Place peaks at higher elevation
        elevs = [2000] * len(lons)
        names = peaks_gdf['name'].tolist() if 'name' in peaks_gdf.columns else ['Peak'] * len(peaks_gdf)
        
        fig.add_trace(go.Scatter3d(
            x=lons,
            y=lats,
            z=elevs,
            mode='markers',
            marker=dict(
                size=8,
                color=MAP_STYLE['mountain_color'],
                symbol='diamond',
                line=dict(color='white', width=2)
            ),
            name='Mountain Peaks',
            text=names,
            hovertemplate='%{text}<br>Elevation: ~%{z:.0f}m<extra></extra>'
        ))
        print(f"  -> Added {len(peaks_gdf)} peaks")
    
    # Update layout for better 3D visualization
    bounds = SALISH_SEA_BOUNDS
    fig.update_layout(
        title={
            'text': 'Salish Sea Watershed - 3D Interactive View',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2D5016'}
        },
        scene=dict(
            xaxis=dict(
                title='Longitude',
                range=[bounds['min_lon'] - 0.5, bounds['max_lon'] + 0.5],
                backgroundcolor=MAP_STYLE['grey_border'],
                gridcolor='white',
                showbackground=True
            ),
            yaxis=dict(
                title='Latitude',
                range=[bounds['min_lat'] - 0.5, bounds['max_lat'] + 0.5],
                backgroundcolor=MAP_STYLE['grey_border'],
                gridcolor='white',
                showbackground=True
            ),
            zaxis=dict(
                title='Elevation (m)',
                range=[0, 2500],
                backgroundcolor='lightgray',
                gridcolor='white',
                showbackground=True
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=2, z=0.5),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
                center=dict(x=0, y=0, z=-0.1)
            )
        ),
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=800,
        hovermode='closest'
    )
    
    # Add annotation
    fig.add_annotation(
        text="Note: Elevation data is synthetic for visualization purposes.<br>Use data download scripts to obtain real SRTM elevation data.",
        xref="paper", yref="paper",
        x=0.5, y=0.02,
        showarrow=False,
        font=dict(size=10, color="gray"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="gray",
        borderwidth=1,
        borderpad=5
    )
    
    # Save as HTML
    output_file = WEB_DIR / 'map_3d.html'
    fig.write_html(
        str(output_file),
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d']
        }
    )
    
    print("\n" + "=" * 60)
    print("3D Map Created Successfully!")
    print("=" * 60)
    print(f"Output: {output_file}")
    print(f"Open this file in a web browser to view the 3D map")
    print("\nInteraction tips:")
    print("  - Click and drag to rotate")
    print("  - Scroll to zoom")
    print("  - Right-click and drag to pan")
    
    return fig


if __name__ == '__main__':
    create_3d_map()
