import numpy as np
import matplotlib.pyplot as plt
import cv2

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

def dist(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def sample_free():
    while True:
        x = np.random.randint(0, map_width)
        y = np.random.randint(0, map_height)
        if is_free(x, y):
            return Node(x, y)

def is_free(x, y):
    return occupancy_grid[y, x] == 0

def nearest(nodes, q_rand):
    return min(nodes, key=lambda node: dist(node, q_rand))

def steer(q_nearest, q_rand, step_size=10):
    theta = np.arctan2(q_rand.y - q_nearest.y, q_rand.x - q_nearest.x)
    new_x = int(q_nearest.x + step_size * np.cos(theta))
    new_y = int(q_nearest.y + step_size * np.sin(theta))
    new_node = Node(new_x, new_y)
    new_node.parent = q_nearest
    return new_node

def collision_free(node1, node2):
    line = cv2.line(np.zeros_like(occupancy_grid), (node1.x, node1.y), (node2.x, node2.y), 1, 1)
    return np.all((line & occupancy_grid) == 0)

def rewire(nodes, new_node, radius=50):
    for node in nodes:
        if dist(node, new_node) < radius and node != new_node.parent:
            if dist(node, new_node) + dist(new_node, new_node.parent) < dist(node, node.parent):
                if collision_free(node, new_node):
                    node.parent = new_node

def get_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node)
        node = node.parent
    return path[::-1]

# Load binary occupancy grid map
img_path = "/home/prathamesh1709/dev_ws/src/basic_mobile_robot/maps/binary_occupancy_grid.png"
occupancy_grid = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded properly
if occupancy_grid is None:
    raise FileNotFoundError(f"Image at path '{img_path}' not found or could not be loaded.")

# Convert the image to a binary occupancy grid (1 for obstacle, 0 for free space)
occupancy_grid = cv2.threshold(occupancy_grid, 127, 255, cv2.THRESH_BINARY)[1]
occupancy_grid = cv2.bitwise_not(occupancy_grid) // 255
map_height, map_width = occupancy_grid.shape

# Start and goal positions
start = Node(50, 50)
goal = Node(950, 950)
nodes = [start]

# RRT* algorithm
max_iterations = 5000
step_size = 10

for i in range(max_iterations):
    q_rand = sample_free()
    q_nearest = nearest(nodes, q_rand)
    q_new = steer(q_nearest, q_rand, step_size)
    
    if collision_free(q_nearest, q_new):
        nodes.append(q_new)
        rewire(nodes, q_new)
        
        if dist(q_new, goal) < step_size:
            goal.parent = q_new
            break

# Extract path
path = get_path(goal)

# Plotting the path
plt.figure()
plt.imshow(occupancy_grid, cmap='gray')
plt.plot([node.x for node in nodes], [node.y for node in nodes], 'yo')
plt.plot([node.x for node in path], [node.y for node in path], 'ro-')
plt.plot(start.x, start.y, 'go')  # Start point
plt.plot(goal.x, goal.y, 'bo')    # End point
plt.title("RRT* Path")
plt.show()


