"""
Mid-360 + D435 together with one RViz view (ADR-005/ADR-007 test).

Run: ros2 launch ~/rover_ws/src/Rover_2/tests/combined/sensors.launch.py [rviz:=false] [jsp:=false]

Sensor frames come from the rover URDF (rover_2 rsp.launch.py):
  base_link -> livox_frame, base_link -> camera_link  (poses in config/sensor_poses.yaml).
joint_state_publisher publishes the (static) wheel joints until ros2_control exists.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

HERE = os.path.dirname(os.path.realpath(__file__))
TESTS = os.path.dirname(HERE)


def generate_launch_description():
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('rover_2'), 'launch', 'rsp.launch.py')),
    )
    jsp = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=IfCondition(LaunchConfiguration('jsp')),
    )
    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(TESTS, 'mid360', 'mid360.launch.py')),
        launch_arguments={'rviz': 'false'}.items(),
    )
    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(TESTS, 'd435', 'd435.launch.py')),
        launch_arguments={'rviz': 'false'}.items(),
    )
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(HERE, 'sensors.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('jsp', default_value='true'),
        rsp, jsp, lidar, camera, rviz,
    ])
