import csv
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
from networkx.algorithms.approximation import traveling_salesman_problem
import matplotlib.pyplot as plt


def TSP_multiple():
    place_name = "Chicago, Illinois, USA"
    G = ox.graph_from_place(place_name, network_type='drive')



    coordinates_list = []

    # Open the CSV file in read mode
    with open('output.csv', 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        ids = []
        temp_coords = []

        for row in csv_reader:
            if len(row) == 1:
                ids.append(row[0])
                if temp_coords:
                    coordinates_list.append(temp_coords)
                temp_coords= []
            else:
                temp_coords.append((float(row[0]), float(row[1])))
        
        # Append the last list of coordinates if it exists
        if temp_coords:
            coordinates_list.append(temp_coords)



    destination_filename = 'open_street_map_tsp_node_data.csv'
    all_routes = [];

    for a in range(len(coordinates_list)):

        try:
            coordinate_tuples = coordinates_list[a]

            hotspot_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in coordinate_tuples]

            distance_matrix = [[0] * len(hotspot_nodes) for _ in range(len(hotspot_nodes))]

            for i, node1 in enumerate(hotspot_nodes):
                for j, node2 in enumerate(hotspot_nodes):
                    if i != j:
                        distance = nx.shortest_path_length(G, node1, node2, weight='length')
                        distance_matrix[i][j] = distance

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
            all_routes.append(routes)


            mode = 'w' if a == 0 else 'a'
            with open(destination_filename, mode, newline='') as destination_file:
                csv_writer = csv.writer(destination_file)
                csv_writer.writerow([ids[a], routes])

            print(f"District {ids[a]} passed")

        except Exception as e:
            print(f"Error processing district {ids[a]}: {e}")