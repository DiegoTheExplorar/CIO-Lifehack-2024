import pandas as pd
import geopandas as gpd

def newHotspotToList():
    importDistricts = 'chicagoPoliceBoundaries.geojson'
    importStations = 'chicagoPoliceStations.csv'
    importClusters = 'Predictions2.csv'

    # Load district data
    districts_data = gpd.read_file(importDistricts)

    # Load police stations CSV
    police_stations = pd.read_csv(importStations)
    police_stations[['longitude', 'latitude']] = police_stations['LOCATION'].apply(lambda x: eval(x)).apply(pd.Series)

    # Convert to GeoDataFrame
    gdf_stations = gpd.GeoDataFrame(
        police_stations, 
        geometry=gpd.points_from_xy(police_stations.longitude, police_stations.latitude)
    )

    # Ensure CRS is set to WGS84 (latitude, longitude)
    if gdf_stations.crs is None:
        gdf_stations.set_crs('EPSG:4326', inplace=True)
    districts_data = districts_data.to_crs(gdf_stations.crs)

    # Spatial join to assign each police station to a district
    gdf_stations['district'] = gpd.sjoin(gdf_stations, districts_data, how='left', predicate='within')['dist_num']

    # Dictionary to hold districts and their corresponding locations
    district_locations = {dist: [] for dist in districts_data['dist_num'].unique()}

    # Place the first police station in each district into the dictionary
    for dist in district_locations:
        filtered_stations = gdf_stations[gdf_stations['district'] == dist]
        if not filtered_stations.empty:
            station = filtered_stations.iloc[0]
            # Store as (latitude, longitude)
            district_locations[dist].append((station['latitude'], station['longitude']))

    # Load patrol locations CSV
    patrol_locations = pd.read_csv(importClusters)
    patrol_locations[['longitude', 'latitude']] = patrol_locations['coordinates'].apply(lambda x: eval(x)).apply(pd.Series)

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
            # Store as (latitude, longitude)
            district_locations[dist].append((row['latitude'], row['longitude']))

    # Write the results to a new CSV file
    with open('crime_hotspots.csv', 'w', newline='') as file:
        for dist, locations in district_locations.items():
            if locations:  # Only write if there are locations (i.e., at least one police station was found)
                # Prepend district ID before locations
                location_strings = [f"{loc[0]:.6f},{loc[1]:.6f}" for loc in locations]
                file.write(f"{dist},{','.join(location_strings)}\n")

    print("Completed writing to crime_hotspots.csv")