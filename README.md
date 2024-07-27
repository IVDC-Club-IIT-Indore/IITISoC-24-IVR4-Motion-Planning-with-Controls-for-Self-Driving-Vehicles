# IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles

## Goal:
To develop a reliable Motion Planner with Control algorithms for collision-free path planning and efficient navigation in a simulated environment.

People Involved : 

Mentors:
- [Arjun S Nair](https://github.com/arjun-593)
- [Ampady B R](https://github.com/ampady06)

Members:
- [Prathamesh Kawtikwar](https://github.com/ppk1709)
- [S Sri Vaishnavi](https://github.com/vaishnavi-1035)
- [Vashista Boddula](https://github.com/Vashista2412)
- [Sanaga Sai Varshini](https://github.com/varshini2902)
- [Sameer Lakkad](https://github.com/sameerlakkad)
<br>

## Tech-Stacks

* ![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

*  ![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-68217A?style=flat&logo=ros&logoColor=white)
)

* ![ROS Noetic](https://img.shields.io/badge/ROS-Noetic-22314E?style=flat&logo=ros&logoColor=white)


* ![Gazebo Classic 11](https://img.shields.io/badge/Gazebo-classic%2011-FF69B4?style=for-the-badge&logo=gazebo&logoColor=white)


* ![Nav2 Stack](https://img.shields.io/badge/Nav2%20Stack-Navigation-2CA9E1?style=flat&logo=ros&logoColor=white)


* ![C++ Badge](https://img.shields.io/badge/C++-blue?style=for-the-badge&logo=c%2B%2B&logoColor=white)

* ![Python Badge](https://img.shields.io/badge/Python-3.x-success?style=for-the-badge&logo=python&logoColor=white)

* ![CasADI](https://img.shields.io/badge/CasADi-0077B5?style=flat&logo=casadi&logoColor=white)



## Implementation:
As an input we were given a world file for the project which looks like this in gazebo
<div style="text-align:centre;">
 <img src="Images/igvc_world.png" alt="Gazebo_world" width="300" height="300">
</div> 

For the above project, we modelled our own 3-wheeled vehicle,
The modelled vehicle has:
1. LiDAR link
2. Camera link
3. IMU link

<div style="display: flex; justify-content: space-around;">
  <img src="Images/soc_bot3.png" alt="Isometric View" width="150" height="150">
  <img src="Images/soc_bot2.png" alt="Side View" width="150" height="150">
  <img src="Images/soc_bot1.png" alt="Front View" width="150" height="150">
</div>


Our first task was to get the map of the above world through SLAM.
For SLAM, we conducted many tests with different robots like:
1. Turtlebot3(Waffle-pi)
2. Atomatic Addison bot
3. Turtlebot3(Burger) for MPC

We conducted SLAM with the following two packages
1. Cartographer(for turtlebot3)
2. SLAM toolbox(For the addison bot)

We got better results with latter, and the map after looked like this(we only mapped the lane in which the robot has to navigate through)

[map_1](maps/my_map.pgm)

To increase the accuracy of the map, we decided to add walls along the lane for the Lidar scans to be more robust and accurate.
For the deployment of walls. we used Gazebo's building editor using the image of the top view of the igvc world as the
[Floor_Plan](Images\ground.png).

With the usage of walls, we got a better [Map](maps\map_soc_walls_3.pgm)

<img src="maps\map-soc-walls-3.png" alt="Map_Final" width="200" height="200">

After getting a fairly accurate map, we moved onto trying path planning algorithms like 
1. RRT
2. Astar
3. Djikstra

### Approach 1:
First we converted our map to a binary occupancy grid given below to make path planning feasible

[Binary occuoancy grid for Approach_1](Images/occupancy_grid_SLAM.png)

With the first approach on the first map(made by the addison bot), we tried plotting waypoints manually to get the results below.

Here's a one with Astar:

<img src="Images/Astar_waypoint.png" alt="Astar algorithm using Waypoint Navigation" width="200" height="200">

### Approach 2:
To make the path planning of the robot completely autonomous,
We have conducted research and finalized two search-based algorithms to determine the best possible path for our project: A* and Dijkstra’s. We compared both algorithms based on several parameters and ultimately chose the path generated by A* as the final one. Overall, A* is often preferred for single-pair shortest pathfinding due to its efficiency and flexibility provided a good heuristic is available.

<img src="Images\Astar Vs Djikstra.jpg" alt="Astar Vs Djikstra" width="300" height="200">

Initially, we had a map generated from a LiDAR scan during SLAM. 

<img src="Path_planning_trials\Binary_Occupancy.png" alt="Binary Occupancy grid" width="200" height="200">

 To prepare the map for pathfinding, we converted all grey pixels (non-black except 254/255) to zero pixels, resulting in a modified map. As A* modifies some elements during its process, we further converted the 254 pixels to 0 and 0 pixels to 254, producing the appropriate map for A*.
We used a waypoint navigation approach to cover the entire area. Our algorithm executes missions autonomously once a set of waypoints is provided from the starting point to the goal in the form of absolute positions (such as GPS coordinates). Waypoint navigation facilitates the completion of the path by achieving shorter goals more easily.
Thus, with Astar, we achieved the following path.
<div style="text-align:center;">
 <img src="Images\Astar_trials.png" alt="Astar Path" width="200" height="200">
</div>
The algorithm encountered difficulties in completing the map if the starting and ending goals were the same. To address this, we introduced intermediate waypoints to guide the algorithm in creating an optimized and shortest path possible.

### MPC Implementation:

For the implementation of an optimal control algorithm for trajectory tracking and planning, we used the MPC (Model Predictive Control) algorithm.

The implementation of Model Predictive Control (MPC) for our project involves a structured approach to ensure accurate path tracking and optimal control. The process can be divided into two main steps: detecting points from the CSV file obtained from path planning and running the MPC code.
#### Detecting Points from the CSV File
Firstly, we need to import and process the CSV file that contains the path planning points. This step involves:

##### Reading the CSV File:
We utilize libraries such as Pandas to load the CSV file, which contains the coordinates of the path points generated during the path planning phase. The points are extracted and stored in arrays for further processing.

#### Running the MPC Code
The next step is to set up and execute the MPC algorithm. This involves defining the system model, setting up the prediction and control horizons, defining the cost function and constraints, and iterating through the path points to control the system.

The Trajectory obtained with this is:

<img src="MPC_results\MPC_Trajectory_1.jpg" alt="MPC_trajectory" width="300" height="200">

##### Set Up the MPC Problem:
We define the state-space representation of the system, including the 
- State transition matrix 
𝐴
, 
- Control input matrix 
𝐵
, 
- Output matrix 
C, and 
- Feedthrough matrix 
D. 

We also set the prediction horizon, control horizon, and define the cost function (matrices 
Q and 𝑅
) along with any constraints on the control inputs and states.

##### Run the MPC Algorithm:
In this step, we loop through the path points, solve the MPC optimization problem at each step, apply the control input to the system, and update the system state accordingly.

This is the working model of the MPC Algorithm on Turtlebot3_Burger:
[MPC_in_action](https://github.com/ppk1709/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/MPC_results/MPC_in_action.mp4)



## References

- M. Abed, B., & M. Jasim, W. (2023). Hybrid approach for multi-objective optimization path planning with moving target. Indonesian Journal of Electrical Engineering and Computer Science, 29(1), 348-357. doi:http://doi.org/10.11591/ijeecs.v29.i1.pp348-357
- https://github.com/richardos/occupancy-grid-a-star/blob/master/a_star.py

- https://github.com/learlinian/UW-Madison-CS540-Introduction-to-AI/blob/master/3.%20A%20Start%20Search.py

- Xiang, Dan & Lin, Hanxi & Ouyang, Jian & Huang, Dan. (2022). Combined improved A* and greedy algorithm for path planning of multi-objective mobile robot. Scientific Reports. 12. 10.1038/s41598-022-17684-0.

- Fareh, Raouf & Baziyad, Mohammed & Rahman, Mohammad & Rabie, Tamer & Bettayeb, Maamar. (2019). Investigating Reduced Path Planning Strategy for Differential Wheeled Mobile Robot. Robotica. 38. 1-21. 10.1017/S0263574719000572.

- https://youtube.com/playlist?list=PLHduviKk47y-E7jyUyQQQlDPxOW5kZo2i&si=uWzSmrtd8PP7DFL5

- [Implement-simultaneous-localization-and-mapping-with-lidar-scans](https://in.mathworks.com/help/nav/ug/implement-simultaneous-localization-and-mapping-with-lidar-scans.html?searchHighlight=Implement%20Simultaneous%20Localization%20And%20Mapping%20%28SLAM%29%20with%20Lidar%20Scans&s_tid=srchtitle_support_results_1_Implement%20Simultaneous%20Localization%20And%20Mapping%20%2528SLAM%2529%20with%20Lidar%20Scans)





