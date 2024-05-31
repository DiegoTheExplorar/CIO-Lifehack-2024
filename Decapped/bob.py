import folium
import requests
import xml.etree.ElementTree as ET
import pandas as pd

def get_coordinates(osm_id):
    # Construct the URL
    url = f"https://api.openstreetmap.org/api/0.6/node/{osm_id}"
    
    # Send the GET request
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.text)
        
        # Extract latitude and longitude
        for node in root.findall('.//node'):
            lat = node.attrib.get('lat')
            lon = node.attrib.get('lon')
            return (float(lat), float(lon))
    else:
        return None

# Load the CSV file to examine its content
file_path = 'new.csv'
data = pd.read_csv(file_path, header=None)

# Create a map centered at a general location
map_osm = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

# Process each district
for index, row in data.iterrows():
    print(f"Processing District {index + 1}")
    # Extract node IDs as a list
    node_ids = eval(row[1])
    
    # Initialize the previous coordinates
    prev_coords = None
    
    # Add markers and lines for each node ID in the district
    for idx, osm_id in enumerate(node_ids):
        coords = get_coordinates(osm_id)
        if coords:
            # Define icon color (red for police stations, blue otherwise)
            if idx == 0 or idx == len(node_ids) - 1:
                icon_color = 'red'
            else:
                icon_color = 'blue'
            
            # Add marker with numbered popup
            popup_text = f"District {index + 1}, Node {idx + 1}: {osm_id}"
            folium.Marker(location=coords, popup=popup_text, icon=folium.Icon(color=icon_color)).add_to(map_osm)
            
            # If not the first point, plot a line from the previous point
            if prev_coords:
                folium.PolyLine(locations=[prev_coords, coords], color='blue').add_to(map_osm)
            
            # Update the previous coordinates
            prev_coords = coords

# Save the map as an HTML file
map_osm.save("osm_ids_map_with_lines.html")
