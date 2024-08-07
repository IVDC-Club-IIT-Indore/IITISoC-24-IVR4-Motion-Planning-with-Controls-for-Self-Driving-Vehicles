# IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles


<details>
  <summary>Table of Contents</summary>
<ul>
  <li><a href="#goal">Goal</a></li>
  <li><a href="#tech-stacks">Tech-Stacks</a></li>
  <li><a href="#implementation">Implementation</a></li>
  <li><a href="#mpc-implementation">MPC Implementation</a></li>
  <li><a href="#complete-roadmap-of-mpc">Complete Roadmap of MPC</a></li>
  <li><a href="#references">References</a></li>
</ul>
</details>


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


* ![ROS Noetic](https://img.shields.io/badge/ROS-Noetic-22314E?style=flat&logo=ros&logoColor=white)


* ![Gazebo Classic 11](https://img.shields.io/badge/Gazebo-classic%2011-FF69B4?style=for-the-badge&logo=gazebo&logoColor=white)


* ![Nav2 Stack](https://img.shields.io/badge/Nav2%20Stack-Navigation-2CA9E1?style=flat&logo=ros&logoColor=white)


* ![C++ Badge](https://img.shields.io/badge/C++-blue?style=for-the-badge&logo=c%2B%2B&logoColor=white)

* ![Python Badge](https://img.shields.io/badge/Python-3.x-success?style=for-the-badge&logo=python&logoColor=white)

* ![CasADI](https://img.shields.io/badge/CasADi-0077B5?style=flat&logo=casadi&logoColor=white)



## Implementation:
As an input we were given a world file for the project which looks like this in gazebo
<div style="text-align:centre;">
 <img src="Images/igvc_world.png" alt="Gazebo_world" width="400" height="400">
</div> 

For the above project, we modelled our own 3-wheeled vehicle,
The modelled vehicle has:
1. LiDAR link
2. IMU link

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
2. SLAM toolbox(For the Addison bot)

We got better results with the former, and the map after looked like this(we only mapped the lane in which the robot has to navigate through and with the usage of SLAM toolbox first.)

We got better results with the SLAM Cartographer method. Cartographer is a real-time simultaneous localization and mapping (SLAM) library developed by Google. It provides high-quality 2D and 3D SLAM solutions that can be used for robotics applications. The Cartographer SLAM method works by using sensor data, such as laser scans and IMU data, to create a map of the environment while simultaneously keeping track of the robot's position within that map.

To increase the accuracy of the map, we decided to add walls along the lane for the Lidar scans to be more robust and accurate.
For the deployment of walls. we used Gazebo's building editor using the image of the top view of the igvc world as the
[Floor_Plan](https://github.com/IVDC-Club-IIT-Indore/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/Images/ground.png).

With the usage of walls, we got a better [Map](https://github.com/IVDC-Club-IIT-Indore/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/maps/map-soc-walls-3.png)

<img src="maps\map-soc-walls-3.png" alt="Map_Final" width="400" height="400">

After getting a fairly accurate map, we moved onto trying path planning algorithms like 
1. Astar
2. Djikstra
3. RRTstar

We had two approaches for Path-planning, one before the mid-eval and then the final approach after the mid-eval as we got more accurate maps in the later half of the project duration.
<p align="right">(<a href="#top">back to top</a>)</p>

### Initial Approach:
First, we converted our map to a binary occupancy grid given below to make path planning feasible

[Binary occupancy grid for Initial_Approach](Images/occupancy_grid_SLAM.png)

With the first approach on the first map(made by the addison bot), we tried plotting waypoints manually to get the results below.

Here's a one with Astar:

<img src="Images/Astar_waypoint.png" alt="Astar algorithm using Waypoint Navigation" width="450" height="400">

### Final Approach:

Finally, we had a map generated from a LiDAR scan during SLAM. 

<img src="Path_planning_trials\map_soc_walls_3_modified.png" alt="Binary Occupancy grid" width="450" height="400">

To prepare the map for pathfinding, we converted all grey pixels (non-black except 254/255) to zero pixels, resulting in a modified map. As A* is modifying white pixels to black and black to white during its process, we further converted the 254(white) pixels to 0(black) and 0 pixels to 254, producing the appropriate map for A*. For, dijkstra's method, we just used the modified map to generate the path. We compared both methods using various parameters to check the best one. The algorithm encountered difficulties in completing the map if the starting and ending goals were the same. To address this, we introduced intermediate waypoints to guide the algorithm in creating an optimized and shortest path possible.

We have conducted research and finalized two search-based algorithms to determine the best possible path for our project: A* and Dijkstra’s. We compared both algorithms based on several parameters and ultimately chose the path generated by A* as the final one. A* is often preferred for single-pair shortest pathfinding due to its efficiency and flexibility provided a good heuristic is available. Finally, A highly optimized fully re-configurable grid-based A* implementation is used for our global planning. It is slightly slower but provides increased quality in paths. 

<table align = "center">
  <thead>
    <tr>
      <th> Parameters </th>
      <th>A*</th>
      <th>Dijkstra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> Computational time </td>
      <td> 7.32 sec </td>
      <td> 5.18 sec </td>
    </tr>
    <tr>
      <td> Path length </td>
      <td> 2481.37 </td>
      <td> 2739.84 </td>
    </tr>
    <tr>
      <td> Path smoothness </td>
      <td> 330.65 </td>
      <td> 815.25 </td>
    </tr>
    <tr>
      <td> Memory usage </td>
      <td> 30.68 MB </td>
      <td> 44.27 MB </td>
    </tr>
    <tr>
      <td> Heuristic </td>
      <td> Yes </td>
      <td> No </td>
    </tr>
    <tr>
      <td> Efficiency </td>
      <td> Faster due to Heuristic </td>
      <td> Can be slower </td>
    </tr>
    <tr>
      <td> Optimality </td>
      <td> Guarentees optimal path if Heuristic is admissable </td>
      <td> Also gives optimal path </td>
    </tr>
    <tr>
      <td> Implementation </td>
      <td> Can be complex due the need of Heuristic </td>
      <td> Simpler to implement </td>
    </tr>
    <tr>
      <td> Used in (generally) </td>
      <td> Robotics, any navigation-based shortest-path problem </td>
      <td> Network routing, GPS systems, any graph-based shortest path problem </td>
    </tr>
    <tr>
      <td> Flexibility </td>
      <td> More flexible due to customizable heuristic </td>
      <td> Less flexible due to lack of heuristic guidance </td>
    </tr>
  </tbody>
</table>
<br>

We used a waypoint navigation approach to cover the entire area. Our algorithm executes missions autonomously once a set of waypoints is provided from the starting point to the goal in the form of absolute positions. Waypoint navigation facilitates the completion of the path by achieving shorter goals more easily.
Thus, with Astar, we achieved the following path.
<div style="text-align:center;">
 <img src="Images\path_visualization.png" alt="Astar Path" width="400" height="400">
</div> 
<p align="right">(<a href="#top">back to top</a>)</p>

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

<img src="MPC_results\MPC_Trajectory_1.jpg" alt="MPC_trajectory" width="800" height="420">

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

### Complete Roadmap of MPC:

###### Library Imports:
Imports necessary libraries including ROS libraries (rospy, geometry_msgs, nav_msgs), CasADi for optimization, and other mathematical utilities.

###### Parameter Initialization:
Sets up various parameters for the MPC such as state and control dimensions, prediction horizon (N), control gains (Q_x, Q_y, Q_theta, R1, R2), and constraints.

###### Global Variables:
Declares global variables to store the current state of the robot (x, y, theta), quaternions (qx, qy, qz, qw), velocity (V), and angular velocity (omega).

###### Callback Functions:
Defines odomfunc to update the robot’s current position and orientation based on odometry data, and pathfunc to update the path for the robot to follow from the Path message.

###### ROS Node and Communication Setup:
Initializes the ROS node, sets up subscribers to the /odom and /my_path topics, and establishes a publisher to the /cmd_vel topic for sending velocity commands to the robot.

###### Path Resolution and Time Step Calculation:
Waits for the path data to be available, then calculates the path resolution and the time step (delta_T) based on the reference velocity (U_ref).

###### MPC Problem Formulation:
Sets up state (x_casadi, y_casadi, theta_casadi) and control (v_casadi, omega_casadi) variables in CasADi, constructs the robot’s motion model using the Runge-Kutta method, and defines the cost function.

States:
- x_casadi
- y_casadi
- theta_casadi

Controls:
- v_casadi
- omega_casadi
  
###### Constraints and Bounds Setup:
Defines constraints and bounds for the optimization problem, ensuring the predicted states and controls remain within specified limits.

###### Optimization and Control Loop:
Continuously solves the optimization problem to find the best control inputs, updates the current state, and publishes control commands (Twist messages) to the robot. The loop iterates until the robot reaches the target path within an allowed error margin.

###### Stopping Condition and Cleanup:
Stops the robot by sending zero velocity commands once the target is reached, prints the total number of MPC iterations, and the total time taken for the path tracking.


This is the working model of the MPC Algorithm on Turtlebot3_Burger:
[MPC_in_action](https://github.com/ppk1709/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/MPC_results/MPC_in_action.mp4)

![gif_MPC](https://github.com/IVDC-Club-IIT-Indore/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/MPC_results/mpc_gif.gif)

Movement of Turtlebot3(Burger) on gazebo using Model Predictive Controls

![gif_2_MPC](https://github.com/IVDC-Club-IIT-Indore/IITISoC-24-IVR4-Motion-Planning-with-Controls-for-Self-Driving-Vehicles/blob/main/MPC_results/mpc_turtlebot.gif)
<p align="right">(<a href="#top">back to top</a>)</p>

## References

- M. Abed, B., & M. Jasim, W. (2023). Hybrid approach for multi-objective optimization path planning with moving target. Indonesian Journal of Electrical Engineering and Computer Science, 29(1), 348-357. doi:http://doi.org/10.11591/ijeecs.v29.i1.pp348-357
- https://github.com/richardos/occupancy-grid-a-star/blob/master/a_star.py

- https://github.com/learlinian/UW-Madison-CS540-Introduction-to-AI/blob/master/3.%20A%20Start%20Search.py

- Xiang, Dan & Lin, Hanxi & Ouyang, Jian & Huang, Dan. (2022). Combined improved A* and greedy algorithm for path planning of multi-objective mobile robot. Scientific Reports. 12. 10.1038/s41598-022-17684-0.

- Fareh, Raouf & Baziyad, Mohammed & Rahman, Mohammad & Rabie, Tamer & Bettayeb, Maamar. (2019). Investigating Reduced Path Planning Strategy for Differential Wheeled Mobile Robot. Robotica. 38. 1-21. 10.1017/S0263574719000572.

- https://youtube.com/playlist?list=PLHduviKk47y-E7jyUyQQQlDPxOW5kZo2i&si=uWzSmrtd8PP7DFL5

- [Implement-simultaneous-localization-and-mapping-with-lidar-scans](https://in.mathworks.com/help/nav/ug/implement-simultaneous-localization-and-mapping-with-lidar-scans.html?searchHighlight=Implement%20Simultaneous%20Localization%20And%20Mapping%20%28SLAM%29%20with%20Lidar%20Scans&s_tid=srchtitle_support_results_1_Implement%20Simultaneous%20Localization%20And%20Mapping%20%2528SLAM%2529%20with%20Lidar%20Scans)

<p align="right">(<a href="#top">back to top</a>)</p>



