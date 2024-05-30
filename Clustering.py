import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
import numpy as np

# Create geometry column
geometry = [Point(xy) for xy in zip(crime_data.longitude, crime_data.latitude)]
gdf = gpd.GeoDataFrame(crime_data, geometry=geometry)

# Prepare data for clustering
X = np.array(list(zip(gdf.longitude, gdf.latitude)))

# DBSCAN clustering
db = DBSCAN(eps=0.01, min_samples=10).fit(X)
labels = db.labels_

# Add cluster labels to GeoDataFrame
gdf['cluster'] = labels

#just to check if code works
print(gdf.head())
