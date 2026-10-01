"""Standalone RealSense D435 test launch (ADR-005).

Run: ros2 launch ~/rover_ws/src/Rover_2/tests/d435/d435.launch.py [rviz:=true]
Wraps realsense2_camera/rs_launch.py. Main topics (namespace /camera/camera):
  color/image_raw, depth/image_rect_raw, aligned_depth_to_color/image_raw, depth/color/points
D435 has no IMU, so gyro/accel stay disabled.
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


def generate_launch_description():
    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')),
        launch_arguments={
            'depth_module.depth_profile': '848,480,30',
            'rgb_camera.color_profile': '1280,720,30',
            'pointcloud.enable': 'true',
            'align_depth.enable': 'true',
            'enable_gyro': 'false',
            'enable_accel': 'false',
        }.items(),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(HERE, 'd435.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='false'),
        camera,
        rviz,
    ])
