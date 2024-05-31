from flask import Flask, request, render_template, redirect, url_for, flash
from markupsafe import Markup
import pandas as pd
import folium
import osmnx as ox
import ast
from Clustering import cluster
from DataCleaning import preprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for flash messages

# Load the data once and use it throughout the app's lifetime
file_path = 'open_street_map_tsp_node_data.csv'
data = pd.read_csv(file_path, header=None)

# Define the place and create the graph from OSMnx
place_name = "Chicago, Illinois, USA"
G = ox.graph_from_place(place_name, network_type='drive')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))

        if file:
            filepath = 'uploaded_file.csv'
            file.save(filepath)
            
            # Process the file and generate the output map
            gdf = cluster(filepath)
            X = pd.get_dummies(gdf['day_of_week'], prefix='day')
            y = gdf['cluster']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
            clf.fit(X_train, y_train)
            
            predictions = clf.predict(X)
            gdf['Predicted_Cluster'] = predictions
            gdf[['latitude', 'longitude']] = gdf[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')
            
            valid_clusters = gdf[gdf['cluster'] != -1]
            cluster_medians = valid_clusters.groupby('cluster')[['latitude', 'longitude']].median().reset_index()
            cluster_medians['Median_Coordinates'] = list(zip(cluster_medians['longitude'], cluster_medians['latitude']))
            
            median_coordinates_only = cluster_medians[['Median_Coordinates']].rename(columns={'Median_Coordinates': 'coordinates'})
            median_coordinates_only.to_csv('Predictions2.csv', index=False)
            
            # Generate the map
            map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)
            coords_list = []
            
            for index, row in median_coordinates_only.iterrows():
                coords = row['coordinates']
                latitude, longitude = coords[1], coords[0]
                folium.Marker([latitude, longitude]).add_to(map)
                coords_list.append((latitude, longitude))
            
            map_html = map._repr_html_()
            
            # Return the HTML response with the embedded map and navigation buttons
            return render_template('map.html', map_html=Markup(map_html))

@app.route('/district', methods=['GET', 'POST'])
def district_index():
    if request.method == 'POST':
        # This block runs when form data is submitted
        district_to_plot = request.form.get('district')
        if district_to_plot:
            return redirect(url_for('display_map', district=district_to_plot))
        else:
            flash('No district selected')
            return redirect(url_for('district_index'))
    else:
        # This block runs when just navigating to the form
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
