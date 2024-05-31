import geopandas as gpd
import pandas as pd
from shapely import wkt
import matplotlib.pyplot as plt




# Load the GeoJSON for district boundaries
districts_data = gpd.read_file('chicagoPoliceBoundaries.geojson')

# Correcting the police stations data
police_stations = pd.read_csv('chicagoPoliceStations.csv')
# Correcting the coordinate parsing to switch to (longitude, latitude)
police_stations['longitude'], police_stations['latitude'] = zip(*police_stations['LOCATION'].apply(lambda x: eval(x)))

# Create GeoDataFrame with correct coordinate order
gdf_stations = gpd.GeoDataFrame(
    police_stations, 
    geometry=gpd.points_from_xy(police_stations.longitude, police_stations.latitude)
)
"""
# Plotting the districts
districts_data.plot(color='blue', alpha=0.5, edgecolor='k')

# Plotting the police stations
gdf_stations.plot(ax=plt.gca(), color='red', markersize=10)

plt.title('Police Stations and District Boundaries')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()
"""
# Ensure CRS is set correctly for both datasets
if gdf_stations.crs is None:
    gdf_stations.set_crs('EPSG:4326', inplace=True)
districts_data = districts_data.to_crs(gdf_stations.crs)

# Perform spatial join
gdf_stations['district'] = gpd.sjoin(gdf_stations, districts_data, how='left', predicate='within')['dist_num']

# Check the results
print(gdf_stations[['latitude', 'longitude', 'district']])
