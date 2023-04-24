import json
import os
import sys

# Set input and output file paths
input_path = sys.argv[1]
output_path = sys.argv[2]

# Open input and output files
with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
    # Loop through input file
    for i, line in enumerate(input_file):
        # Load JSON object
        obj = json.loads(line)
        # Write JSON object to output file
        output_file.write(json.dumps(obj) + '\n')
        # Check if we have written 1000 objects
        if i == 999:
            break
