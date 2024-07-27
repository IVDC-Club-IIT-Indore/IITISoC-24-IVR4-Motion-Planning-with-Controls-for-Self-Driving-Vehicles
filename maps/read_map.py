import yaml
import numpy as np
import cv2

yaml_file_path = "/home/prathamesh1709/dev_ws/src/basic_mobile_robot/maps/my_map.yaml"
with open(yaml_file_path, 'r') as file:
    map_metadata = yaml.safe_load(file)


pgm_file_path = map_metadata['image']
occupancy_grid = cv2.imread(pgm_file_path,cv2.IMREAD_GRAYSCALE)

occupancy_grid = cv2.bitwise_not(occupancy_grid)

_, binary_map = cv2.threshold(occupancy_grid, 60, 255, cv2.THRESH_BINARY)

binary_map = binary_map // 255

print(binary_map)
print(occupancy_grid)