"""
Read yaml from path and write json to path
"""
import yaml
import json

# Define the file paths
yaml_file_path = '../xy/xy-lib/gcp/cloud_functions/rpc_proxy/dev_rpc_endpoints.json'
json_file_path = 'endpoints.json'

# Read the YAML file
with open(yaml_file_path, 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Convert YAML data to JSON
json_data = json.dumps(yaml_data, indent=2)

# Write JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"YAML content from '{yaml_file_path}' has been converted to JSON and saved to '{json_file_path}'.")
