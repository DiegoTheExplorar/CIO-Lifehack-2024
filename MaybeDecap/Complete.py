from Clustering import cluster
from DataCleaning import preprocess
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import joblib
from tqdm import tqdm

# Load the clustered GeoDataFrame
gdf = cluster('City_of_Chicago_Crime_Data.csv')

# Prepare feature matrix X using one-hot encoding for 'day_of_week'
X = pd.get_dummies(gdf['day_of_week'], prefix='day')

# Target variable y is the cluster labels
y = gdf['cluster']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

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
median_coordinates_only.to_csv('Predictions2.csv', index=False)

print("Done!")

