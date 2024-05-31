import folium
import osmnx as ox
import pandas as pd
import ast  # Safe evaluation of strings containing Python expressions

# Define the place and create the graph from OSMnx
place_name = "Chicago, Illinois, USA"
G = ox.graph_from_place(place_name, network_type='drive')

# Initialize the Folium map centered around a general location
center_coords = (41.8781, -87.6298)
map_osm = folium.Map(location=center_coords, zoom_start=12)

# Load the CSV file to examine its content
file_path = 'open_street_map_tsp_node_data.csv'
data = pd.read_csv(file_path, header=None)

# Specify the district number to plot
district_to_plot = 20  # Change this to the desired district number
print('parsed')
# Process each node ID listed in the CSV
for index, row in data.iterrows():
    # Check if the current row's district matches the district to plot
    if int(row[0]) == district_to_plot:
        # Extract the node IDs from the string in the second column
        node_ids = ast.literal_eval(row[1])  # Safely evaluate the string to a Python list
        prev_coords = None  # Initialize previous coordinates
        for idx, osm_id in enumerate(node_ids):
            try:
                node_data = G.nodes[osm_id]
                coords = (node_data['y'], node_data['x'])
                # Define icon color (red for first and last nodes, blue otherwise)
                if idx == 0 or idx == len(node_ids) - 1:
                    icon_color = 'red'
                else:
                    icon_color = 'blue'
                # Add marker with numbered popup
                popup_text = f"District {district_to_plot}, Node {idx + 1}: {osm_id}"
                folium.Marker(location=coords, popup=popup_text, icon=folium.Icon(color=icon_color)).add_to(map_osm)
                # If not the first point, plot a line from the previous point
                if prev_coords:
                    folium.PolyLine(locations=[prev_coords, coords], color='blue').add_to(map_osm)
                # Update the previous coordinates
                prev_coords = coords
            except KeyError:
                print(f"Node ID {osm_id} not found in the graph.")

# Save the map
map_osm.save('nodes_from_csv_map.html')
