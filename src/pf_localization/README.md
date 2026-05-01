# pf_localization

ROS 2 Python package for PF-based localization using wireless RSSI observations and robot motion data.

This package is part of my master’s thesis implementation inspired by CDoA-based localization.

## What It Does

- Subscribes to wireless quality measurements (`WirelessLink`)
- Subscribes to robot odometry and velocity topics
- Runs PF-related localization logic in `pf_localization.py`
- Provides a ROS 2 launch file for running the localization node

## Package Contents

```text
pf_localization/
  launch/pf_localization.launch.py
  pf_localization/pf_localization.py
  package.xml
  setup.py
```

## Dependencies

Declared ROS dependencies include:
- `rclpy`
- `std_msgs`
- `geometry_msgs`
- `nav_msgs`

Runtime message dependency from sibling package:
- `ros2_network_analysis` (for `WirelessLink` messages used in code)

## Build

From repository root:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Run

**Important**: You need to run EKF localization for the filtered odometry data. Run the following command to get the topic ```odometry/filtered```
```bash
ros2 launch roverrobotics_driver robot_localizer.launch.py
```

Launch:

```bash
ros2 launch pf_localization pf_localization.launch.py
```

Or run directly:

```bash
ros2 run pf_localization pf_localization
```

## Robot Bring-Up Reference 

Use these commands as the robot-side bring-up reference before or during localization experiments.

### Robot access

```bash
ssh -X rover@192.168.1.91    # MAX
ssh -X rover@192.168.1.100   # Mini
ssh -X husarion@192.168.1.51 # Husarion
```

### Drivers and basic control (For Rover Robot Max)

```bash
ros2 launch roverrobotics_driver max.launch.py
```
Use this only when there's an issue with the startup. When turning on the robot, wait for 30 seconds. This will automatically run the driver, and you can use the PS4 controller for teleop. 

### SLAM / mapping stack

Run these commands on separate terminals

```bash
ros2 launch roverrobotics_driver slam_launch.py
```
```bash
ros2 launch realsense2_camera rs_launch.py depth_module depth_profile:=640x480x30 rgb_camera color_profile:=640x480x30
```
```bash
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link camera_link
```
```bash
ros2 launch rtabmap_launch rtabmap.launch.py rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/camera/depth/image_rect_raw rgb_topic:=/camera/camera/color/image_raw camera_info_topic:=/camera/camera/color/camera_info approx_sync:=true
```

Alternative RTAB-Map timing setting from the same reference:

```bash
ros2 launch rtabmap_launch rtabmap.launch.py rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/camera/depth/image_rect_raw rgb_topic:=/camera/camera/color/image_raw camera_info_topic:=/camera/camera/color/camera_info approx_sync:=true approx_sync_max_interval:=0.015
```

### Navigation

```bash
ros2 launch roverrobotics_driver navigation_launch.py
```

To avoid controller crashing, use:

```bash
ros2 launch roverrobotics_driver navigation_launch.py map_file_name:=/home/rover/test_maps/my_map use_respawn:=True autostart:=false
```

Or with explicit map argument:

```bash
ros2 launch roverrobotics_driver navigation_launch.py map:=/home/rover/maps/hero_map_new.yaml
```

### Useful checks

```bash
rviz2
ls -l /dev/serial/by-id/
eog map.pgm
```

## Important Topics

The code currently subscribes to:
- `/node1/network_analysis/wireless_quality`
- `/node2/network_analysis/wireless_quality`
- `/node3/network_analysis/wireless_quality`
- `/node4/network_analysis/wireless_quality`
- `/odometry/wheels`
- `/cmd_vel`

The launch file parameters currently include:
- `rssi_topic`
- `odom_topic`
- `cmd_vel_topic`

Update these values to match your robot setup before running experiments.

## Notes

- Package metadata still has placeholder maintainer values.
- This is an active research codebase and will continue to evolve.
