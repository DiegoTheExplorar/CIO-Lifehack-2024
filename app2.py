from flask import Flask, render_template, request, redirect, url_for
import folium
import osmnx as ox
import pandas as pd
import ast

app = Flask(__name__)

# Load the data once and use it throughout the app's lifetime
file_path = 'open_street_map_tsp_node_data.csv'
data = pd.read_csv(file_path, header=None)

# Define the place and create the graph from OSMnx
place_name = "Chicago, Illinois, USA"
G = ox.graph_from_place(place_name, network_type='drive')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        district_to_plot = int(request.form['district'])
        return redirect(url_for('display_map', district=district_to_plot))
    # Extracting unique districts from the CSV
    districts = sorted(set(data[0].astype(int)))
    return render_template('index2.html', districts=districts)

@app.route('/map/<district>')
def display_map(district):
    center_coords = (41.8781, -87.6298)
    map_osm = folium.Map(location=center_coords, zoom_start=12)
    district_to_plot = int(district)

    # Filter and plot the nodes for the selected district
    selected_rows = data[data[0] == district_to_plot]
    for index, row in selected_rows.iterrows():
        node_ids = ast.literal_eval(row[1])
        prev_coords = None
        for idx, osm_id in enumerate(node_ids):
            try:
                node_data = G.nodes[osm_id]
                coords = (node_data['y'], node_data['x'])
                icon_color = 'red' if idx == 0 or idx == len(node_ids) - 1 else 'blue'
                popup_text = f"District {district_to_plot}, Node {idx + 1}: {osm_id}"
                folium.Marker(location=coords, popup=popup_text, icon=folium.Icon(color=icon_color)).add_to(map_osm)
                if prev_coords:
                    folium.PolyLine(locations=[prev_coords, coords], color='blue').add_to(map_osm)
                prev_coords = coords
            except KeyError:
                print(f"Node ID {osm_id} not found in the graph.")
    # Save the map into HTML string
    map_html = map_osm._repr_html_()
    return render_template('map2.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
