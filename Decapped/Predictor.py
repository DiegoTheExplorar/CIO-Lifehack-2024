import pandas as pd
import joblib

# Load the clustered GeoDataFrame
print("Loading data...")
gdf = pd.read_csv('clustered_data2.csv')

# Prepare features
print("Preparing features...")
X = pd.get_dummies(gdf['day_of_week'], prefix='day')

# Load the Random Forest model
print("Loading Random Forest model...")
clf = joblib.load('random_forest_model2.joblib')

# Predict clusters
print("Predicting clusters...")
predictions = clf.predict(X)

# Add predictions to the DataFrame
gdf['Predicted_Cluster'] = predictions

# Ensure latitude and longitude columns are numeric
print("Ensuring latitude and longitude columns are numeric...")
gdf[['latitude', 'longitude']] = gdf[['latitude', 'longitude']].apply(pd.to_numeric, errors='coerce')

# Filter out the -1 clusters and calculate median coordinates for each cluster
print("Calculating median coordinates for each cluster...")
valid_clusters = gdf[gdf['cluster'] != -1]
cluster_medians = valid_clusters.groupby('cluster')[['latitude', 'longitude']].median().reset_index()

# Create a single column with (longitude, latitude) tuples
cluster_medians['Median_Coordinates'] = list(zip(cluster_medians['longitude'], cluster_medians['latitude']))

# Keep only the 'Median_Coordinates' column and rename it to 'Coordinates'
median_coordinates_only = cluster_medians[['Median_Coordinates']].rename(columns={'Median_Coordinates': 'coordinates'})

# Save combined data to a CSV file
print("Saving combined data...")
median_coordinates_only.to_csv('Predictions.csv', index=False)

print("Done!")
