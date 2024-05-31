import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import joblib
from tqdm import tqdm

# Load the clustered GeoDataFrame
gdf = pd.read_csv('clustered_data2.csv')

# Prepare feature matrix X using one-hot encoding for 'day_of_week'
X = pd.get_dummies(gdf['day_of_week'], prefix='day')

# Target variable y is the cluster labels
y = gdf['cluster']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save the Random Forest model immediately after training
joblib.dump(clf, 'random_forest_model2.joblib')
print("Model saved successfully.")
