import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
import numpy as np
from DataCleaning import preprocess

def cluster(file):
    crime_data = preprocess(file)
    print('Started Cluster Function')
    # Create geometry column
    geometry = [Point(xy) for xy in zip(crime_data.longitude, crime_data.latitude)]
    gdf = gpd.GeoDataFrame(crime_data, geometry=geometry)
    print('Prepared Data for clustering')
    # Prepare data for clustering
    X = np.array(list(zip(gdf.longitude, gdf.latitude)))
    print('Starting DBSCAN')
    # DBSCAN clustering
    db = DBSCAN(eps=0.0015, min_samples=5).fit(X)
    labels = db.labels_
    print('Finished DBSCAN')
    # Add cluster labels to GeoDataFrame
    gdf['cluster'] = labels

    # Save the clustered GeoDataFrame
    #gdf.to_csv('clustered_data2.csv', index=False)
    #print(f'Clustered data saved')
    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print("Number of clusters:", num_clusters)

    # Just to check if code works
    print(gdf.head())
    print('DBSCAN done')
    return gdf

