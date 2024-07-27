import yaml
import numpy as np
import cv2
import os

# Load the YAML file
yaml_file_path = '/home/prathamesh1709/dev_ws/src/basic_mobile_robot/maps/my_map.yaml'
with open(yaml_file_path, 'r') as file:
    map_metadata = yaml.safe_load(file)

# Get the directory of the YAML file
yaml_dir = os.path.dirname(yaml_file_path)

# Load the PGM file (handle relative path)
pgm_file_path = os.path.join(yaml_dir, map_metadata['image'])
occupancy_grid = cv2.imread(pgm_file_path, cv2.IMREAD_GRAYSCALE)

# Normalize pixel values to range [0, 1]
occupancy_grid = occupancy_grid / 255.0

# Convert thresholds to float
occupied_thresh = float(map_metadata['occupied_thresh'])
free_thresh = float(map_metadata['free_thresh'])

# Apply the thresholds
binary_map = np.zeros_like(occupancy_grid, dtype=np.uint8)
binary_map[occupancy_grid > occupied_thresh] = 1
binary_map[occupancy_grid < free_thresh] = 0

# Print the binary map
print(binary_map)
