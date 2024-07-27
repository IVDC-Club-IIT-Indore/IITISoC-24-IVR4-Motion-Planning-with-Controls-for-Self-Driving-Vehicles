#!/usr/bin/env python3
import csv
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

def main():
    rospy.init_node('csv_to_path_publisher')

    # Parameterize the file path
    csv_file_path = rospy.get_param('~csv_file_path', '/home/sameer/igvc/src/pathdiv.csv')

    # Create publisher for path message
    path_pub = rospy.Publisher('my_path', Path, queue_size=10)

    # Initialize empty path message
    path = Path()
    path.header.frame_id = rospy.get_param('~frame_id', 'map')  # Set the frame id, change as needed

    try:
        # Read CSV data
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row_number, row in enumerate(reader, start=1):
                try:
                    # Assuming format: X, Y, (optional)timestamp
                    x = float(row[0])
                    y = float(row[1])

                    # Extract timestamp if present (modify based on your CSV format)
                    if len(row) > 2:
                        timestamp = float(row[2])
                    else:
                        timestamp = rospy.get_rostime().to_sec()  # Use current ROS time as float

                    # Create PoseStamped message for this data point
                    pose = PoseStamped()
                    pose.pose.position.x = x
                    pose.pose.position.y = y
                    # Set orientation (yaw) to 0 for simplicity (modify if needed)
                    pose.pose.orientation.w = 1.0  # Represents no rotation (quaternion)
                    pose.header.stamp = rospy.Time.from_sec(timestamp) if isinstance(timestamp, (float, int)) else timestamp  # Set timestamp

                    # Append PoseStamped message to the path
                    path.poses.append(pose)

                except ValueError as e:
                    rospy.logerr(f"Error parsing row {row_number} in CSV file: {row} - {e}")

    except FileNotFoundError:
        rospy.logerr(f"CSV file not found: {csv_file_path}")
        return

    # Publish the complete path message at a rate of 10 Hz
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        path.header.stamp = rospy.Time.now()  # Update the header timestamp
        path_pub.publish(path)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
