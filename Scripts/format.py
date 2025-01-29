"""
This script provides a function to format a GeoJSON file by cleaning up unnecessary whitespace,
structuring the data for better readability, and ensuring consistent spacing between numerical values.

Function:
    format(input_file, output_file): Reads a GeoJSON file, formats its content, and writes the formatted
                                     content to a new file.

Parameters:
    - input_file (str): Path to the input GeoJSON file.
    - output_file (str): Path to the output file where the formatted content will be saved.

Steps:
1. Read the input file content while preserving UTF-8 encoding.
2. Remove all newline characters, tab characters, and extra spaces.
3. Add newlines and spaces to key sections to improve readability:
   - Format the structure of the GeoJSON, including "FeatureCollection" and "features".
   - Clean and restructure "Feature" properties and coordinates.
4. Use a regular expression to add spaces between latitude and longitude pairs.
5. Write the formatted content to the specified output file.
6. Print a success message upon successful formatting.
7. Catch and display any errors encountered during file processing.

Usage:
    - Update the `input_geojson` and `output_geojson` variables with the file paths.
    - Call the `format()` function to process the input GeoJSON and save the formatted file.
"""

import re

def format(input_file, output_file):
    try:
        # Read the content of the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove unnecessary whitespace
        content = content.replace("\n", "").replace("\t", "").replace("  ", "")

        # Add newlines after the opening curly brace
        content = content.replace("{", "{\n", 1)

        # Add newline after the "FeatureCollection" declaration
        content = content.replace('"type": "FeatureCollection",', ' "type": "FeatureCollection",\n', 1)

        # Add a newline before the "features" array
        content = content.replace('"features": [', ' "features": [\n', 1)

        # Format the properties section of each feature
        content = content.replace('{"type": "Feature","properties": {"fid":', '{ "type": "Feature", "properties": { "fid":')

        # Add a space before the "cat" key for better alignment
        content = content.replace(',"cat":', ', "cat":')

        # Add a space before the "init_node" key for better alignment
        content = content.replace(',"init_node":', ', "init_node":')

        # Add a space before the "term_node" key for better alignment
        content = content.replace(',"term_node":', ', "term_node":')

        # Add a space before the "capacity" key for better alignment
        content = content.replace(',"capacity":', ', "capacity":')

        # Add a space before the "length" key for better alignment
        content = content.replace(',"length":', ', "length":')

        # Format the geometry section of each feature
        content = content.replace('},"geometry": {"type": "LineString","coordinates": [[', '}, "geometry": { "type": "LineString", "coordinates": [ [ ')
        
        # Add spaces around coordinate pairs
        content = content.replace('],[', ' ], [ ')

        # Add newlines and spaces to close each feature correctly
        content = content.replace(']]}},', ' ] ] } },\n')

        # Add final newlines and spaces to close the entire features array and FeatureCollection
        content = content.replace(']]}}]}', ' ] ] } }\n]\n}')

        # Ensure proper spacing in coordinate pairs
        content = re.sub(r'(-?\d+\.\d+),(-?\d+\.\d+)', r'\1, \2', content)

        # Write the formatted content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"File successfully formatted: {output_file}")

    except Exception as e:
        # Handle and display any errors during processing
        print(f"Error processing the file: {e}")

# Define input and output file paths
input_geojson = "network30000_480000.geojson"  # Replace this with the name of your input file
output_geojson = "formated_network30000_480000.geojson"
format(input_geojson, output_geojson)
