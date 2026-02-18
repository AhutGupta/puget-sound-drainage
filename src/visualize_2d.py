"""
Create 2D interactive map of Salish Sea region using Folium
"""

import os
from pathlib import Path
import geopandas as gpd
import folium
from folium import plugins

# Import config
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import SALISH_SEA_BOUNDS, MAP_STYLE, WEB_CONFIG, POPULATION_CONFIG

# Setup paths
BASE_DIR = Path(__file__).parent.parent
DATA_PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
WEB_DIR = BASE_DIR / 'web'
WEB_DIR.mkdir(exist_ok=True)


def create_base_map():
    """Create base Folium map"""
    print("Creating base map...")
    
    # Create map centered on Salish Sea
    m = folium.Map(
        location=[WEB_CONFIG['center_lat'], WEB_CONFIG['center_lon']],
        zoom_start=WEB_CONFIG['default_zoom'],
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    return m


def add_boundary_layer(m):
    """Add grey boundary for context area"""
    print("Adding boundary layer...")
    
    try:
        # Create expanded boundary for grey area
        bounds = SALISH_SEA_BOUNDS
        expanded_bounds = {
            'min_lon': bounds['min_lon'] - 2,
            'max_lon': bounds['max_lon'] + 2,
            'min_lat': bounds['min_lat'] - 2,
            'max_lat': bounds['max_lat'] + 2
        }
        
        # Create grey rectangle for surrounding area
        grey_area = folium.Rectangle(
            bounds=[
                [expanded_bounds['min_lat'], expanded_bounds['min_lon']],
                [expanded_bounds['max_lat'], expanded_bounds['max_lon']]
            ],
            color=MAP_STYLE['grey_border'],
            fill=True,
            fillColor=MAP_STYLE['grey_border'],
            fillOpacity=0.3,
            weight=0,
            popup='Surrounding Region'
        )
        grey_area.add_to(m)
        
        # Add focus area boundary
        focus_boundary = folium.Rectangle(
            bounds=[
                [bounds['min_lat'], bounds['min_lon']],
                [bounds['max_lat'], bounds['max_lon']]
            ],
            color=MAP_STYLE['boundary_color'],
            fill=False,
            weight=3,
            dashArray='5, 5',
            popup='Salish Sea Focus Area'
        )
        focus_boundary.add_to(m)
        
        print("  -> Added boundary layers")
        
    except Exception as e:
        print(f"  -> Error adding boundary: {e}")


def add_geojson_layer(m, filename, layer_name, color, feature_group=None):
    """Add a GeoJSON layer to the map"""
    print(f"Adding {layer_name} layer...")
    
    try:
        filepath = DATA_PROCESSED_DIR / filename
        
        if not filepath.exists():
            print(f"  -> File not found: {filename}")
            return
        
        gdf = gpd.read_file(filepath)
        
        if len(gdf) == 0:
            print(f"  -> No features in {filename}")
            return
        
        # Create feature group if not provided
        if feature_group is None:
            feature_group = folium.FeatureGroup(name=layer_name, show=True)
        
        # Add GeoJSON to map
        folium.GeoJson(
            gdf,
            name=layer_name,
            style_function=lambda x: {
                'color': color,
                'weight': 2,
                'fillColor': color,
                'fillOpacity': 0.6
            },
            highlight_function=lambda x: {
                'weight': 3,
                'fillOpacity': 0.8
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['name'] if 'name' in gdf.columns else [],
                aliases=['Name:'] if 'name' in gdf.columns else [],
                style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            )
        ).add_to(feature_group)
        
        feature_group.add_to(m)
        
        print(f"  -> Added {len(gdf)} {layer_name} features")
        
    except Exception as e:
        print(f"  -> Error adding {layer_name}: {e}")


def add_point_layer(m, filename, layer_name, color):
    """Add a point layer to the map"""
    print(f"Adding {layer_name} layer...")
    
    try:
        filepath = DATA_PROCESSED_DIR / filename
        
        if not filepath.exists():
            print(f"  -> File not found: {filename}")
            return
        
        gdf = gpd.read_file(filepath)
        
        if len(gdf) == 0:
            print(f"  -> No features in {filename}")
            return
        
        # Create feature group
        feature_group = folium.FeatureGroup(name=layer_name, show=True)
        
        # Add markers
        for idx, row in gdf.iterrows():
            popup_text = row.get('name', 'Unknown')
            if 'elevation' in row and row['elevation']:
                popup_text += f"<br>Elevation: {row['elevation']}m"
            
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=5,
                popup=popup_text,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(feature_group)
        
        feature_group.add_to(m)
        
        print(f"  -> Added {len(gdf)} {layer_name} features")
        
    except Exception as e:
        print(f"  -> Error adding {layer_name}: {e}")


def add_populated_places_layer(m, filename, layer_name, color):
    """Add populated places with labels to the map"""
    print(f"Adding {layer_name} layer...")
    
    try:
        filepath = DATA_PROCESSED_DIR / filename
        
        if not filepath.exists():
            print(f"  -> File not found: {filename}")
            return
        
        gdf = gpd.read_file(filepath)
        
        if len(gdf) == 0:
            print(f"  -> No features in {filename}")
            return
        
        # Create feature group
        feature_group = folium.FeatureGroup(name=layer_name, show=True)
        
        # Add markers with labels
        for idx, row in gdf.iterrows():
            name = row.get('name', 'Unknown')
            popup_text = f"<b>{name}</b>"
            
            if 'population' in row and row['population']:
                pop = int(row['population'])
                popup_text += f"<br>Population: {pop:,}"
            
            if 'country' in row and row['country']:
                popup_text += f"<br>Country: {row['country']}"
            
            # Size marker based on population
            if 'population' in row and row['population']:
                pop = int(row['population'])
                if pop > 500000:
                    radius = 10
                elif pop > 100000:
                    radius = 7
                else:
                    radius = 5
            else:
                radius = 5
            
            # Add circle marker
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=radius,
                popup=popup_text,
                tooltip=name if POPULATION_CONFIG['label_places'] else None,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8,
                weight=2
            ).add_to(feature_group)
        
        feature_group.add_to(m)
        
        print(f"  -> Added {len(gdf)} {layer_name} features")
        
    except Exception as e:
        print(f"  -> Error adding {layer_name}: {e}")


def add_title_and_legend(m):
    """Add title and legend to the map"""
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 60px; width: 400px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
                border-radius: 5px;">
        <h3 style="margin: 0; padding: 0; color: #2D5016;">Salish Sea Watershed Map</h3>
        <p style="margin: 5px 0; padding: 0; font-size: 12px;">
            Interactive visualization of Puget Sound, Georgia Strait, and surrounding watershed
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Add legend
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 10px; width: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
                border-radius: 5px;">
        <h4 style="margin: 0 0 10px 0; color: #333;">Legend</h4>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['salish_sea_color']}; width: 20px; height: 10px; display: inline-block;"></i>
            Salish Sea
        </p>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['river_color']}; width: 20px; height: 10px; display: inline-block;"></i>
            Rivers & Streams
        </p>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['forest_color']}; width: 20px; height: 10px; display: inline-block;"></i>
            Forests
        </p>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['mountain_color']}; width: 20px; height: 10px; display: inline-block;"></i>
            Mountain Peaks
        </p>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['city_color']}; width: 20px; height: 10px; display: inline-block;"></i>
            Cities & Towns (pop &gt; 10K)
        </p>
        <p style="margin: 5px 0;">
            <i style="background:{MAP_STYLE['grey_border']}; width: 20px; height: 10px; display: inline-block; opacity: 0.3;"></i>
            Surrounding Areas
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))


def create_2d_map():
    """Create the complete 2D map"""
    print("=" * 60)
    print("Creating 2D Salish Sea Map")
    print("=" * 60)
    
    # Create base map
    m = create_base_map()
    
    # Add boundary layer (grey surrounding area)
    add_boundary_layer(m)
    
    # Add data layers in order (back to front)
    add_geojson_layer(m, 'coastlines.geojson', 'Coastlines', MAP_STYLE['salish_sea_color'])
    add_geojson_layer(m, 'rivers.geojson', 'Major Rivers', MAP_STYLE['river_color'])
    add_geojson_layer(m, 'osm_waterways.geojson', 'Streams & Waterways', MAP_STYLE['river_color'])
    add_geojson_layer(m, 'osm_forests.geojson', 'Forests', MAP_STYLE['forest_color'])
    add_point_layer(m, 'osm_peaks.geojson', 'Mountain Peaks', MAP_STYLE['mountain_color'])
    add_populated_places_layer(m, 'populated_places.geojson', 'Populated Places', MAP_STYLE['city_color'])
    
    # Add title and legend
    add_title_and_legend(m)
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # Add minimap
    minimap = plugins.MiniMap(toggle_display=True)
    m.add_child(minimap)
    
    # Add layer control (must be added after all layers are added)
    folium.LayerControl(position='topright').add_to(m)
    
    # Save map
    output_file = WEB_DIR / 'map_2d.html'
    m.save(str(output_file))
    
    print("\n" + "=" * 60)
    print("2D Map Created Successfully!")
    print("=" * 60)
    print(f"Output: {output_file}")
    print(f"Open this file in a web browser to view the map")
    
    return m


if __name__ == '__main__':
    create_2d_map()
