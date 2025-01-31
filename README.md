In this repository are available scripts in Python for creation and formatting of 
graphs in GeoJSON format, compatible with the graph partitioning program. Additionally, a 
script to process the partitions obtained and get different parameters of comparison between 
the original graph and the partitions obtained with the different algorithms used.

To use the scripts in this repository you need to have Python 3 pre-installed on your system.

Mode of use: generate the graphs according to number of nodes and edges needed with generate_geojson.py, format it using format.py before inserting it in graph partitioning program, 
Otherwise it will not recognize the nodes or edges. You can then parse the partitions in relation to the original graph using partitions_quality.py. Examples of use are found
in the documentation of each of the scripts.
