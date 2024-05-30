import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load the clustered GeoDataFrame
gdf = pd.read_csv('gdf.csv')

X = pd.get_dummies(gdf['day_of_week'], prefix='day')
y = gdf['cluster']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on the test set
predictions = clf.predict(X_test)

# Evaluate the model
print(classification_report(y_test, predictions))

# Calculate median coordinates for each cluster
cluster_medians = gdf.groupby('cluster').median()[['latitude', 'longitude']]

# Map predicted clusters to their median coordinates
predicted_coords = pd.DataFrame(predictions, columns=['cluster']).merge(cluster_medians, how='left', left_on='cluster', right_index=True)

# Save the results
results_df = X_test.copy()
results_df['Actual_Cluster'] = y_test
results_df['Predicted_Cluster'] = predictions
results_df = results_df.reset_index().merge(predicted_coords, how='left', on='cluster')
results_df.rename(columns={'latitude': 'Predicted_Latitude', 'longitude': 'Predicted_Longitude'}, inplace=True)
results_df.to_csv('cluster_predictions_with_median_coords.csv', index=False)

