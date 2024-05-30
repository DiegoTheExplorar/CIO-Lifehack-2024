import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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

# Filter out points belonging to cluster -1
print("Filtering out points belonging to cluster -1...")
cluster_minus_1 = gdf[gdf['cluster'] == -1][['cluster', 'latitude', 'longitude']]

# Calculate median coordinates for each cluster (excluding -1)
print("Calculating median coordinates for each cluster...")
cluster_medians = gdf.groupby('cluster')[['latitude', 'longitude']].median().reset_index()
cluster_medians['Cluster_Label'] = cluster_medians['cluster']

# Combine cluster medians with cluster -1 points
print("Combining cluster medians with cluster -1 points...")
combined_data = pd.concat([cluster_medians, cluster_minus_1], ignore_index=True)

# Save combined data to a CSV file
print("Saving combined data...")
combined_data.to_csv('bob.csv', index=False)
