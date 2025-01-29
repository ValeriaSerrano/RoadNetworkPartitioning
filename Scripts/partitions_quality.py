"""
This script analyzes node partitions in a graph by extracting unique nodes from multiple files, 
counting the number of nodes in each partition, calculating the difference between the largest 
and smallest partition, and identifying the number of edges cut between partitions.

Functions:
    - extract_unique_nodes_from_multiple_files(files): 
        Extracts unique node identifiers from a list of GeoJSON partition files.
    - count_nodes_in_partitions_and_diff(nodes_by_partition): 
        Counts the number of nodes in each partition and calculates the difference 
        between the largest and smallest partition.
    - count_edges_in_cut_and_max_partition(original_graph_file, nodes_by_partition): 
        Counts the number of edges in the cut (edges that connect nodes in different partitions) 
        and identifies the partition with the most cut edges.

Steps:
1. Extract unique nodes from each partition file:
   - Reads each file line by line.
   - Uses regex to find `"init_node"` and `"term_node"` values.
   - Stores unique nodes for each partition.
2. Count the number of nodes in each partition and calculate the difference between the 
   maximum and minimum number of nodes.
3. Count the number of edges in the cut:
   - Reads the original graph file.
   - Checks if an edge connects nodes in different partitions.
   - Counts edges that connect nodes belonging to different partitions.
4. Identify the partition with the highest number of cut edges.

Output:
    - A dictionary mapping each partition file to its list of unique nodes.
    - The number of nodes in each partition.
    - The difference between the largest and smallest partition.
    - The number of edges in the cut for each partition.
    - The partition with the most cut edges.

Example Usage:
    - Define the original graph file and partition files.
    - Extract nodes from partitions.
    - Count nodes per partition and calculate the difference.
    - Count cut edges and identify the partition with the most cut edges.
"""

import re

def extract_unique_nodes_from_multiple_files(files):
    """
    Extracts unique node identifiers from multiple GeoJSON partition files.

    Args:
        files (list): A list of file paths containing partitioned graph data.

    Returns:
        dict: A dictionary mapping each file path to a list of unique node identifiers.
    """
    all_nodes = {}

    try:
        for file_path in files:
            unique_nodes_set = set()  # Set to store unique nodes per partition

            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    # Extract node identifiers using regex
                    match_init = re.search(r'"init_node":\s*([\d.]+)', line)
                    if match_init:
                        unique_nodes_set.add(match_init.group(1))

                    match_term = re.search(r'"term_node":\s*([\d.]+)', line)
                    if match_term:
                        unique_nodes_set.add(match_term.group(1))

            all_nodes[file_path] = list(unique_nodes_set)  # Store nodes for each partition

        return all_nodes
    except Exception as e:
        print(f"Error processing files: {e}")
        return all_nodes




def count_nodes_in_partitions_and_diff(nodes_by_partition):
    """
    Counts the number of nodes in each partition and calculates the difference 
    between the largest and smallest partition.

    Args:
        nodes_by_partition (dict): A dictionary mapping each partition file to its node list.

    Returns:
        tuple: (A dictionary with node counts per partition, difference between max and min nodes).
    """
    node_counts = {}

    for file, nodes in nodes_by_partition.items():
        node_counts[file] = len(nodes)  # Count nodes in each partition

    max_nodes = max(node_counts.values())  # Largest partition
    min_nodes = min(node_counts.values())  # Smallest partition
    diff = max_nodes - min_nodes  # Difference between largest and smallest

    return node_counts, diff




def count_edges_in_cut_and_max_partition(original_graph_file, nodes_by_partition):
    """
    Counts the number of edges in the cut (edges that connect nodes in different partitions)
    and identifies the partition with the most cut edges.

    Args:
        original_graph_file (str): Path to the original graph file.
        nodes_by_partition (dict): A dictionary mapping partition files to their node lists.

    Returns:
        tuple: (A dictionary with cut edge counts per partition, partition with the most cut edges).
    """
    cut_edges_count = {file: 0 for file in nodes_by_partition}  # Initialize edge count per partition
   
    try:
        with open(original_graph_file, 'r', encoding='utf-8') as file:
            graph_data = file.readlines()  # Read the entire graph file

            for line in graph_data:
                line = line.strip()

                # Extract init and term node identifiers using regex
                match_init = re.search(r'"init_node":\s*([\d.]+)', line)
                match_term = re.search(r'"term_node":\s*([\d.]+)', line)

                if match_init and match_term:
                    init_node = match_init.group(1)
                    term_node = match_term.group(1)
                    
                    # Count cut edges for each partition
                    for file, nodes in nodes_by_partition.items():
                        if init_node in nodes and term_node not in nodes:  
                            cut_edges_count[file] += 1
                        elif term_node in nodes and init_node not in nodes:
                            cut_edges_count[file] += 1

        # Identify the partition with the most cut edges
        max_partition = max(cut_edges_count, key=cut_edges_count.get)
        
        return cut_edges_count, max_partition

    except Exception as e:
        print(f"Error processing the original graph file: {e}")
        return cut_edges_count, None


# Example Usage
original_graph_file = "formated_network30000_480000.geojson"  # Path to the original graph file
files = ["Partition0_0.geojson", 
         "Partition0_1.geojson", 
         "Partition0_2.geojson", 
         "Partition0_3.geojson",
         "Partition0_4.geojson", 
         "Partition0_5.geojson", 
         "Partition0_6.geojson", 
         "Partition0_7.geojson"
         ]  # List of partitioned graph files

# Extract unique nodes for each partition
nodes_by_partition = extract_unique_nodes_from_multiple_files(files)

# Display unique nodes per partition
# for file, nodes in nodes_by_partition.items():
#     print(f"Unique nodes in {file}: {nodes}")

# Count nodes per partition and calculate the difference
node_counts, diff = count_nodes_in_partitions_and_diff(nodes_by_partition)

# Display the number of nodes per partition
for file, count in node_counts.items():
    print(f"Number of nodes in {file}: {count}")

# Display the difference between the largest and smallest partition
print(f"Difference between the largest and smallest partition: {diff}")

# Count cut edges and identify the partition with the most cut edges
cut_edges, max_partition = count_edges_in_cut_and_max_partition(original_graph_file, nodes_by_partition)

# Display the number of cut edges per partition
for file, count in cut_edges.items():
    print(f"Number of cut edges in {file}: {count}")

# Display the partition with the most cut edges
print(f"The partition with the most cut edges is: {max_partition} with {cut_edges[max_partition]} edges.")
