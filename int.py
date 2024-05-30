import pandas as pd
import folium

# Load CSV file
data = pd.read_csv('bob_with_coordinates.csv')

# Create a map centered around Chicago
map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

# Function to parse coordinates and create markers
def plot_points(row):
    coords = row['coordinates'].strip('()').split(', ')
    latitude = float(coords[0])
    longitude = float(coords[1])
    folium.Marker([latitude, longitude]).add_to(map)

# Apply the function to each row in the dataframe
data.apply(plot_points, axis=1)

# Save the map to an HTML file
map.save('map.html')
