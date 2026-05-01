# src Workspace Guide

This directory contains the ROS 2 packages used in this thesis project:
- `pf_localization`
- `ros2_network_analysis` (folder name: `ros2-network-analysis`)

## Prerequisites

- ROS 2 installation sourced in your shell
- `colcon`
- Python 3
- Linux network tools needed by network analysis scripts:

```bash
sudo apt-get install -y net-tools ethtool
```

## Build the Workspace

Run from the repository root:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Run the System (Typical Flow)

Open multiple terminals and source the workspace in each terminal:

```bash
source install/setup.bash
```

### 1) Start wireless quality publisher

```bash
ros2 run ros2_network_analysis wireless_quality.py
```

### 2) (Optional) Start other network diagnostics

```bash
ros2 run ros2_network_analysis link_utilization.py
ros2 run ros2_network_analysis network_errors.py
```

### 3) (Optional) Start network delay service/client pair

Service terminal:

```bash
ros2 run ros2_network_analysis network_ping_service
```

Client terminal:

```bash
ros2 run ros2_network_analysis network_ping_client
```

### 4) Start PF localization

```bash
ros2 launch pf_localization pf_localization.launch.py
```

## Multi-Robot Localization Deployment (4 Raspberry Pi 5 Nodes)


### 1) SSH into each wireless node

Use a terminal per node:

```bash
ssh <user>@<node_ip_or_hostname>
```

Password for each node:

```text
herolab
```

Reference robot access from `robots_launch_instructions.txt`:

```bash
ssh -X rover@192.168.1.91    # MAX
ssh -X rover@192.168.1.100   # Mini
ssh -X husarion@192.168.1.51 # Husarion
```

Optional robot bring-up reference commands:

```bash
ros2 launch roverrobotics_driver max.launch.py
ros2 launch roverrobotics_driver slam_launch.py
ros2 launch realsense2_camera rs_launch.py depth_module.depth_profile:=640x480x30 rgb_camera.color_profile:=640x480x30
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link camera_link
ros2 launch rtabmap_launch rtabmap.launch.py rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/camera/depth/image_rect_raw rgb_topic:=/camera/camera/color/image_raw camera_info_topic:=/camera/camera/color/camera_info approx_sync:=true
ros2 launch roverrobotics_driver navigation_launch.py map_file_name:=/home/rover/test_maps/my_map use_respawn:=True autostart:=false
```

### 2) On each Raspberry Pi 5 node, source ROS 2 Jazzy

```bash
source /opt/ros/jazzy/setup.bash
```

If running from this workspace on the node, also source the local overlay:

```bash
source ~/cdoa-ros2/install/setup.bash
```

### 3) Start ROS 2 network analysis on each node

At minimum, start wireless quality publishing:

```bash
ros2 run ros2_network_analysis wireless_quality.py
```

Optional diagnostics per node:

```bash
ros2 run ros2_network_analysis link_utilization.py
ros2 run ros2_network_analysis network_errors.py
```

### 4) On either robot, run PF localization

On MAX or the other robot terminal:

**Important**: You need to run EKF localization for the filtered odometry data. Run the following command to get the topic ```odometry/filtered```
```bash
ros2 launch roverrobotics_driver robot_localizer.launch.py
```
```bash
source /opt/ros/jazzy/setup.bash
source ~/cdoa-ros2/install/setup.bash
ros2 launch pf_localization pf_localization.launch.py
```

### 5) Verify topic alignment before experiments

`pf_localization` currently expects per-node topics (for example `/node1/...` to `/node4/...`) in code, while the launch default is `/network_analysis/wireless_quality`.
Align topics in:
- `pf_localization/launch/pf_localization.launch.py`
- `pf_localization/pf_localization/pf_localization.py`

## Topic Alignment Note

`pf_localization` currently subscribes to per-node wireless topics such as:
- `/node1/network_analysis/wireless_quality`
- `/node2/network_analysis/wireless_quality`
- `/node3/network_analysis/wireless_quality`
- `/node4/network_analysis/wireless_quality`

Its launch file currently defaults to:
- `/network_analysis/wireless_quality`

Before experiments, align topic names in:
- `pf_localization/launch/pf_localization.launch.py`
- `pf_localization/pf_localization/pf_localization.py`

## Package Docs

- PF localization details: [pf_localization/README.md](pf_localization/README.md)
- Network analysis details: [ros2-network-analysis/README.md](ros2-network-analysis/README.md)
