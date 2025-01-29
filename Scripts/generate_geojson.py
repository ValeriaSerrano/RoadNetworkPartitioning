"""
This script generates a GeoJSON network with a specified number of nodes and edges. 
It randomly assigns coordinates to nodes and creates edges connecting these nodes, 
including random properties like capacity and length for each edge.

Function:
    generate_geojson(num_nodes, num_edges): Creates a GeoJSON object representing a network 
                                            with the given number of nodes and edges.

Parameters:
    - num_nodes (int): The number of nodes (points) in the network.
    - num_edges (int): The number of edges (connections) between nodes in the network.

Steps:
1. Validate the input to ensure the number of edges does not exceed the maximum possible 
   edges for the given number of nodes in an undirected graph.
2. Generate random geographic coordinates for each node:
   - Longitude ranges from -180 to 180 degrees.
   - Latitude ranges from -90 to 90 degrees.
3. Randomly select pairs of nodes to create unique edges without repetition.
4. For each edge, create a GeoJSON feature with the following:
   - Properties: Includes `fid`, `init_node`, `term_node`, `capacity` (random float between 100 and 1000), 
     and `length` (random float between 0.1 and 10).
   - Geometry: A `LineString` with coordinates for the start and end nodes.
5. Compile all features into a GeoJSON FeatureCollection and return the result.

Output:
    - A GeoJSON object containing nodes and edges of the network.
    - The result can be saved to a file for use in mapping or spatial analysis.

Example Usage:
    - Specify the number of nodes (`num_nodes`) and edges (`num_edges`).
    - Call the `generate_geojson()` function to create the network.
    - Save the resulting GeoJSON to a file.

"""

import json
import random

def generate_geojson(num_nodes, num_edges):
    # Validate input: Ensure the number of edges does not exceed the possible connections
    if num_edges > num_nodes * (num_nodes - 1) // 2:
        raise ValueError("Too many edges for the given number of nodes.")

    # Initialize the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate random coordinates for each node
    nodes = {
        i: [
            round(random.uniform(-18000, 18000), 6),  # Longitude with 6 decimal places
            round(random.uniform(-9000, 9000), 6)    # Latitude with 6 decimal places
        ]
        for i in range(1, num_nodes + 1)
    }

    # Generate unique edges between nodes
    edges = set()
    while len(edges) < num_edges:
        init_node, term_node = random.sample(list(nodes.keys()), 2)  # Randomly pick two distinct nodes
        # Ensure no duplicate edges (e.g., (A, B) and (B, A))
        if (init_node, term_node) not in edges and (term_node, init_node) not in edges:
            edges.add((init_node, term_node))

    # Create GeoJSON features for each edge
    for fid, (init_node, term_node) in enumerate(edges, start=1):
        feature = {
            "type": "Feature",
            "properties": {
                "fid": fid,  # Feature ID
                "cat": fid,  # Category (same as fid)
                "init_node": init_node,  # Starting node of the edge
                "term_node": term_node,  # Ending node of the edge
                "capacity": round(random.uniform(100, 1000), 1),  # Random capacity
                "length": round(random.uniform(0.1, 10), 2)  # Random length
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    nodes[init_node],  # Start node coordinates
                    nodes[term_node]  # End node coordinates
                ]
            }
        }
        # Add the feature to the GeoJSON
        geojson["features"].append(feature)

    return geojson

# Example usage
if __name__ == "__main__":
    num_nodes = 30000  # Number of nodes in the network
    num_edges = 480000  # Number of the edges in the network

    # Generate the GeoJSON network
    geojson_network = generate_geojson(num_nodes, num_edges)

    # Save the GeoJSON to a file
    output_path = "network30000_480000.geojson"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(geojson_network, file, ensure_ascii=False, indent=4)

    print(f"GeoJSON network with {num_nodes} nodes and {num_edges} edges saved to {output_path}.")
