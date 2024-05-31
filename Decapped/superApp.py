import os
import pandas as pd
import geopandas as gpd
import folium
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from shapely.geometry import Point
from flask_cors import CORS
import csv
import osmnx as ox
import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem
import ast

app = Flask(__name__, static_folder='templates')
CORS(app)

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading the CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')
        file.save(filepath)
        
        # Process the file and generate the output map
        gdf = preprocess_and_cluster(filepath)
        gdf = predict_clusters(gdf)
        save_cluster_medians(gdf)
        
        generate_map(gdf)
        
        return render_template('map.html')

# Function to preprocess the data and perform clustering
def preprocess_and_cluster(filepath):
    crime_data = pd.read_csv(filepath)

    # Data cleaning and preprocessing (assuming the function 'preprocess' exists)
    # You can replace this with the actual preprocessing steps
    def preprocess(data):
        def parse_date(date_str):
            try:
                return pd.to_datetime(date_str, format='%m/%d/%Y %I:%M:%S %p')
            except ValueError:
                return pd.to_datetime(date_str, format='%m/%d/%y %H:%M')

        data['date_time'] = data['Date'].apply(parse_date)

        def parse_location(location_str):
            if pd.isna(location_str):
                return None, None
            match = re.match(r'\(([^,]+), ([^,]+)\)', location_str)
            if match:
                return float(match.group(1)), float(match.group(2))
            return None, None

        data[['latitude', 'longitude']] = data['Location'].apply(lambda loc: pd.Series(parse_location(loc)))
        data.dropna(subset=['latitude', 'longitude'], inplace=True)

        data['date'] = data['date_time'].dt.date
        data['time'] = data['date_time'].dt.time
        data['day_of_week'] = data['date_time'].dt.dayofweek
        data['month'] = data['date_time'].dt.month
        data['hour'] = data['date_time'].dt.hour
        data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

        return data

    crime_data = preprocess(crime_data)

    # Clustering using DBSCAN
    geometry = [Point(xy) for xy in zip(crime_data.longitude, crime_data.latitude)]
    gdf = gpd.GeoDataFrame(crime_data, geometry=geometry)
    X = np.array(list(zip(gdf.longitude, gdf.latitude)))
    db = DBSCAN(eps=0.01, min_samples=10).fit(X)
    gdf['cluster'] = db.labels_
    
    return gdf

# Function to predict clusters using a RandomForestClassifier
def predict_clusters(gdf):
    X = pd.get_dummies(gdf['day_of_week'], prefix='day')
    y = gdf['cluster']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    predictions = clf.predict(X)
    gdf['Predicted_Cluster'] = predictions
    gdf[['latitude', 'longitude']] = gdf[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')
    
    return gdf

# Function to save the cluster medians to a CSV file
def save_cluster_medians(gdf):
    valid_clusters = gdf[gdf['cluster'] != -1]
    cluster_medians = valid_clusters.groupby('cluster')[['latitude', 'longitude']].median().reset_index()
    cluster_medians['Median_Coordinates'] = list(zip(cluster_medians['longitude'], cluster_medians['latitude']))
    
    median_coordinates_only = cluster_medians[['Median_Coordinates']].rename(columns={'Median_Coordinates': 'coordinates'})
    median_coordinates_only.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'Predictions2.csv'), index=False)

# Function to generate the map with the cluster medians
def generate_map(gdf):
    map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)
    coords_list = []
    cluster_medians = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'Predictions2.csv'))
    cluster_medians[['longitude', 'latitude']] = cluster_medians['coordinates'].apply(lambda x: eval(x)).apply(pd.Series)
    
    for index, row in cluster_medians.iterrows():
        coords = (row['latitude'], row['longitude'])
        folium.Marker([coords[0], coords[1]]).add_to(map)
        coords_list.append((coords[0], coords[1]))
    
    map.save(os.path.join(app.static_folder, 'map.html'))

# Route to display the districts and patrol routes
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

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
