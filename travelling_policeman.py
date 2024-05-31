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
    #print(row)
    pass



# Create a complete graph from the distance matrix
complete_graph = nx.complete_graph(len(hotspot_nodes))
nx.set_edge_attributes(complete_graph, {(i, j): distance_matrix[i][j] for i in range(len(hotspot_nodes)) for j in range(len(hotspot_nodes)) if i != j}, 'weight')



# Solve the TSP using the approximation algorithm
tsp_path = traveling_salesman_problem(complete_graph, cycle=True)
tsp_cycle = [hotspot_nodes[i] for i in tsp_path]



# Extract the paths between consecutive nodes in the TSP cycle
routes = []
for i in range(len(tsp_cycle) - 1):
    route = nx.shortest_path(G, tsp_cycle[i], tsp_cycle[i + 1], weight='length')
    routes.extend(route[:-1])  # Avoid duplicate nodes except the last one

# Add the path from the last node back to the first to complete the cycle
final_leg = nx.shortest_path(G, tsp_cycle[-1], tsp_cycle[0], weight='length')
routes.extend(final_leg)

fig, ax = ox.plot_graph_route(G, routes, route_linewidth=1, node_size=0, bgcolor='k', orig_dest_size=0, route_color='r')
fig.savefig("chicago_tsp_route.png", dpi=1000)
plt.show()