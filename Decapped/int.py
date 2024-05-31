import pandas as pd
import folium

# Load CSV file
data = pd.read_csv('Predictions2.csv')

# Create a map centered around Chicago
map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

# Function to parse coordinates and create markers
def plot_points(row, coords_list):
    coords = row['coordinates'].strip('()').split(', ')
    latitude = float(coords[1])
    longitude = float(coords[0])
    folium.Marker([latitude, longitude]).add_to(map)
    coords_list.append((latitude, longitude))

# List to store coordinates
coords_list = []

# Apply the function to each row in the dataframe
data.apply(lambda row: plot_points(row, coords_list), axis=1)

# Add lines between points
folium.PolyLine(coords_list, color='blue').add_to(map)

# Save the map to an HTML file
map.save('map.html')
