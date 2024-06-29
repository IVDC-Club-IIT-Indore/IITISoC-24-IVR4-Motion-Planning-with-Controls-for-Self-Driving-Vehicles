import yaml
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the YAML file
def load_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Load the PGM file and convert to numpy array
def load_pgm(pgm_file):
    img = Image.open(pgm_file)
    return np.array(img)

# Create the occupancy grid
def create_occupancy_grid(pgm_array, yaml_data):
    resolution = yaml_data['resolution']
    origin = yaml_data['origin']
    negate = yaml_data['negate']
    occupied_thresh = yaml_data['occupied_thresh']
    free_thresh = yaml_data['free_thresh']
    
    # Convert PGM values to occupancy values
    if negate:
        pgm_array = 255 - pgm_array
    
    occupancy_grid = np.zeros_like(pgm_array, dtype=float)
    occupancy_grid[pgm_array > (occupied_thresh * 255)] = 1.0
    occupancy_grid[pgm_array < (free_thresh * 255)] = 0.0
    occupancy_grid[(pgm_array >= (free_thresh * 255)) & (pgm_array <= (occupied_thresh * 255))] = -1.0
    
    return occupancy_grid

# Display the occupancy grid
def display_occupancy_grid(occupancy_grid, resolution, origin):
    plt.imshow(occupancy_grid, cmap='gray')
    plt.title('Occupancy Grid')
    plt.show()

# Example usage
yaml_file = '/home/prathamesh1709/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/maps/my_map.yaml'  # replace with your yaml file path
pgm_file = '/home/prathamesh1709/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/maps/my_map.pgm'    # replace with your pgm file path

yaml_data = load_yaml(yaml_file)
pgm_array = load_pgm(pgm_file)
occupancy_grid = create_occupancy_grid(pgm_array, yaml_data)

display_occupancy_grid(occupancy_grid, yaml_data['resolution'], yaml_data['origin'])
