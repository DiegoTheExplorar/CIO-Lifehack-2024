import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Define the place name for Chicago
place_name = "Chicago, Illinois, USA"

# Download the graph data for the specified place
G = ox.graph_from_place(place_name, network_type='drive')

# Define the start and end locations (latitude, longitude)
start_point = (41.8781, -87.6298)  # Example coordinates for downtown Chicago
end_point = (41.881832, -87.623177)  # Example coordinates for Millennium Park

# Find the nearest nodes in the graph for the start and end points
start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

# Calculate the shortest path between the start and end nodes
route = nx.shortest_path(G, start_node, end_node, weight='length')
print(route)

# Plot the graph with the route, without highlighting start/end nodes
fig, ax = ox.plot_graph_route(
    G, 
    route, 
    route_linewidth=1, 
    node_size=0, 
    bgcolor='k', 
    route_color='y', 
    orig_dest_size=0  # Set node size to 0 to avoid highlighting
)

# Save the plot to a file with high resolution
fig.savefig("chicago_route.png", dpi=1000)
plt.show()
