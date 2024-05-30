import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
from networkx.algorithms.approximation import traveling_salesman_problem
import matplotlib.pyplot as plt

crime_hotspots = [
    (40.748817, -73.985428),  # Example coordinates (latitude, longitude)
    (40.712776, -74.005974),
    (40.730610, -73.935242),
    (40.729517, -73.998649),  # Additional hotspots to ensure multiple routes
    (40.758896, -73.985130)
]

# Define the central point for creating the graph
central_point = (sum(lat for lat, lon in crime_hotspots) / len(crime_hotspots),
                 sum(lon for lat, lon in crime_hotspots) / len(crime_hotspots))

# Create the graph for the specified area
G = ox.graph_from_point(central_point, dist=5000, network_type='drive')

# Find the nearest nodes in the graph for each crime hotspot
hotspot_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in crime_hotspots]

# Initialize the distance matrix
distance_matrix = [[0] * len(hotspot_nodes) for _ in range(len(hotspot_nodes))]

# Calculate the shortest path distance between each pair of nodes
for i, node1 in enumerate(hotspot_nodes):
    for j, node2 in enumerate(hotspot_nodes):
        if i != j:
            distance = nx.shortest_path_length(G, node1, node2, weight='length')
            distance_matrix[i][j] = distance

# Print the distance matrix
for row in distance_matrix:
    print(row)

# Create a complete graph from the distance matrix
complete_graph = nx.complete_graph(len(hotspot_nodes))
nx.set_edge_attributes(complete_graph, {(i, j): distance_matrix[i][j] for i in range(len(hotspot_nodes)) for j in range(len(hotspot_nodes)) if i != j}, 'weight')

# Solve the TSP using the approximation algorithm
tsp_path = traveling_salesman_problem(complete_graph, cycle=True)

# Print the TSP path
print("Optimized Patrol Route:", tsp_path)

# Convert the TSP path into actual route nodes
route_nodes = [hotspot_nodes[i] for i in tsp_path]

# Ensure the route is correctly interpreted as a list of routes
routes = [route_nodes] * 5

# Plot the routes
fig, ax = ox.plot_graph_routes(G, routes, route_linewidth=6, node_size=0, bgcolor='k')
plt.show()
