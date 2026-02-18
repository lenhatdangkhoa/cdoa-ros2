from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pf_localization',
            executable='pf_localization',
            name='pf_localization',
            output='screen',
            parameters=[{
                # If you have a Float32 RSSI topic, set this:
                #'rssi_float_topic': '/node1/network_analysis/wireless_quality/rssi',
                # If you have a custom WirelessLink msg in ROS2, set this (and enable in code):
                'rssi_topic': '/network_analysis/wireless_quality',
                'odom_topic': '/odom',
                'cmd_vel_topic': '/cmd_vel',
            }]
        )
    ])
