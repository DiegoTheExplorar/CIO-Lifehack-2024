from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import folium
from Clustering import cluster
from DataCleaning import preprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
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
        #This is where Chicago is can be changed to Singapore
        map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)
        coords_list = []
        
        for index, row in median_coordinates_only.iterrows():
            coords = row['coordinates']
            latitude, longitude = coords[1], coords[0]
            folium.Marker([latitude, longitude]).add_to(map)
            coords_list.append((latitude, longitude))
        
        #folium.PolyLine(coords_list, color='blue').add_to(map)
        map.save('templates/map.html')
        
        return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
