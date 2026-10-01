"""
Standalone Livox Mid-360 test launch (ADR-005).

Run: ros2 launch ~/rover_ws/src/Rover_2/tests/mid360/mid360.launch.py [rviz:=true]
Publishes /livox/lidar (sensor_msgs/PointCloud2, PointXYZRTLT) and /livox/imu.
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

HERE = os.path.dirname(os.path.realpath(__file__))


def generate_launch_description():
    driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        output='screen',
        parameters=[{
            'xfer_format': 0,        # 0 = PointCloud2 (PointXYZRTLT), 1 = Livox CustomMsg
            'multi_topic': 0,
            'data_src': 0,
            'publish_freq': 10.0,
            'output_data_type': 0,
            'frame_id': 'livox_frame',
            'user_config_path': os.path.join(HERE, 'MID360_config.json'),
            'cmdline_input_bd_code': 'livox0000000001',
        }],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(HERE, 'mid360.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='false'),
        driver,
        rviz,
    ])
