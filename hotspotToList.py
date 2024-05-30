import geopandas as gpd
import pandas as pd
from shapely import wkt

# Load district data
districts_data = gpd.read_file('chicagoPoliceBoundaries.geojson')

# Load police stations CSV
police_stations = pd.read_csv('chicagoPoliceStations.csv')
# Assuming tuple in 'coordinates' column as "(lat, lon)"
police_stations['latitude'], police_stations['longitude'] = zip(*police_stations['LOCATION'].apply(lambda x: eval(x)))

# Convert to GeoDataFrame
gdf_stations = gpd.GeoDataFrame(
    police_stations, 
    geometry=gpd.points_from_xy(police_stations.longitude, police_stations.latitude)
)

if gdf_stations.crs is None:
    gdf_stations.set_crs('EPSG:4326', inplace=True)
districts_data = districts_data.to_crs(gdf_stations.crs)

# (this is a spatial join) Assign each police station to the first matching district
gdf_stations['district'] = gpd.sjoin(gdf_stations, districts_data, how='left', predicate='within')['dist_num']

# Create a dictionary to hold districts and their corresponding locations
district_locations = {dist: [] for dist in districts_data['dist_num'].unique()}

# Place the first police station in each district into the dictionary
for dist in district_locations:
    filtered_stations = gdf_stations[gdf_stations['district'] == dist]
    if not filtered_stations.empty:
        station = filtered_stations.iloc[0]
        district_locations[dist].append((station['latitude'], station['longitude']))
    else:
        print(f"No police stations found in district {dist}")

# Load patrol locations CSV
patrol_locations = pd.read_csv('cleanedSample.csv')  # Assuming column 'coordinates'
# Splitting tuple stored as string in 'coordinates' into latitude and longitude
patrol_locations['latitude'], patrol_locations['longitude'] = zip(*patrol_locations['coordinates'].apply(lambda x: eval(x)))

# Convert to GeoDataFrame
gdf_patrols = gpd.GeoDataFrame(
    patrol_locations, 
    geometry=gpd.points_from_xy(patrol_locations.longitude, patrol_locations.latitude)
)

# Assign patrol locations to districts
gdf_patrols['district'] = gpd.sjoin(gdf_patrols, districts_data, how='left', predicate='within')['dist_num']

# Add patrol locations to the corresponding districts in the dictionary
for index, row in gdf_patrols.iterrows():
    dist = row['district']
    if dist in district_locations:
        district_locations[dist].append((row['latitude'], row['longitude']))

# Write the results to a new CSV file
with open('district_patrols.csv', 'w') as file:
    for dist, locations in district_locations.items():
        # Convert all tuples to string and concatenate them with comma
        location_strings = ['{:.6f},{:.6f}'.format(lat, lon) for lat, lon in locations]
        file.write(f"{dist},{' '.join(location_strings)}\n")

print("Completed writing to district_patrols.csv")
