# ros2_network_analysis

ROS 2 package for monitoring wireless network quality and communication performance between robots and/or control stations.

This package provides reusable measurement nodes for:
- Wireless quality (RSSI, LQI, noise, link status)
- Throughput and link utilization
- Network error counters
- Service-based ping delay measurement

## Package Role in This Project

In this thesis workspace, this package provides the wireless/network measurements consumed by localization experiments, including PF-based localization in `pf_localization`.

## Build

From repository root:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Run Nodes

### Wireless quality (RSSI/LQI/noise)

```bash
ros2 run ros2_network_analysis wireless_quality.py
```

Default publish topic in script:
- `node1/network_analysis/wireless_quality`

### Link utilization

```bash
ros2 run ros2_network_analysis link_utilization.py
```

Default publish topic:
- `network_analysis/link_utilization`

### Network errors

```bash
ros2 run ros2_network_analysis network_errors.py
```

Default publish topic:
- `network_analysis/network_errors`

### Network delay (service + client)

Start service:

```bash
ros2 run ros2_network_analysis network_ping_service
```

Start client:

```bash
ros2 run ros2_network_analysis network_ping_client
```

Service name:
- `network_analysis/ping`

Client publish topic:
- `network_analysis/network_delay`

## Interfaces

This package defines custom interfaces in:
- `msg/`
- `srv/`

Key message types include:
- `WirelessLink`
- `WirelessLinkVector`
- `LinkUtilization`
- `NetworkErrors`
- `NetworkDelay`
- `NetworkAnalysis`

## System Dependencies

Some scripts rely on Linux tools and files such as:
- `netstat`
- `ethtool`
- `/proc/net/wireless`
- `/proc/net/dev`
- `/proc/net/snmp`

Install tools:

```bash
sudo apt-get install -y net-tools ethtool
```

## Legacy Launch Files

The package includes XML launch files in `launch/` from the original project workflow. In this ROS 2 workspace, direct `ros2 run` commands (shown above) are the reliable baseline path.

## Citation

If you use this network analysis package in academic work, please cite:

Pandey, P., and Parasuraman, R., "Empirical Analysis of Bi-directional Wi-Fi Network Performance on Mobile Robots in Indoor Environments," 2022 IEEE 95th Vehicular Technology Conference (VTC2022-Spring), 2022, pp. 1-7, doi:10.1109/VTC2022-Spring54318.2022.9860438.

Link:
- https://ieeexplore.ieee.org/abstract/document/9860438
