import csv
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
from networkx.algorithms.approximation import traveling_salesman_problem
import matplotlib.pyplot as plt

place_name = "Chicago, Illinois, USA"
G = ox.graph_from_place(place_name, network_type='drive')

coordinates = []

# Open the CSV file in read mode
with open('district_patrols1.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    for row in csv_reader:
        coordinates.append(row)
    
coordinate_tuples = [(float(row[0]), float(row[1])) for row in coordinates]

hotspot_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in coordinate_tuples]

distance_matrix = [[0] * len(hotspot_nodes) for _ in range(len(hotspot_nodes))]

for i, node1 in enumerate(hotspot_nodes):
    for j, node2 in enumerate(hotspot_nodes):
        if i != j:
            distance = nx.shortest_path_length(G, node1, node2, weight='length')
            distance_matrix[i][j] = distance

for row in distance_matrix:
    print(row)
