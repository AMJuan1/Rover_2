"""Mid-360 + D435 together with one RViz view (ADR-005/ADR-007 test).

Run: ros2 launch ~/rover_ws/src/Rover_2/tests/combined/sensors.launch.py [rviz:=false]
     optional camera pose relative to the LiDAR (placeholder, not calibrated):
     cam_x:=0.10 cam_y:=0.0 cam_z:=-0.05 cam_roll:=0 cam_pitch:=0 cam_yaw:=0  (m, rad)

Frames: livox_frame (fixed) -> camera_link via a static transform.
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

HERE = os.path.dirname(os.path.realpath(__file__))
TESTS = os.path.dirname(HERE)

CAM_POSE = {
    'cam_x': '0.10', 'cam_y': '0.0', 'cam_z': '-0.05',
    'cam_roll': '0.0', 'cam_pitch': '0.0', 'cam_yaw': '0.0',
}


def generate_launch_description():
    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(TESTS, 'mid360', 'mid360.launch.py')),
        launch_arguments={'rviz': 'false'}.items(),
    )
    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(TESTS, 'd435', 'd435.launch.py')),
        launch_arguments={'rviz': 'false'}.items(),
    )

    lidar_to_camera = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='livox_to_camera_tf',
        arguments=[
            '--x', LaunchConfiguration('cam_x'),
            '--y', LaunchConfiguration('cam_y'),
            '--z', LaunchConfiguration('cam_z'),
            '--roll', LaunchConfiguration('cam_roll'),
            '--pitch', LaunchConfiguration('cam_pitch'),
            '--yaw', LaunchConfiguration('cam_yaw'),
            '--frame-id', 'livox_frame',
            '--child-frame-id', 'camera_link',
        ],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(HERE, 'sensors.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    args = [DeclareLaunchArgument('rviz', default_value='true')]
    args += [DeclareLaunchArgument(k, default_value=v) for k, v in CAM_POSE.items()]

    return LaunchDescription(args + [lidar, camera, lidar_to_camera, rviz])
