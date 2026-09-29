# Rover

Autonomous ground rover built on ROS 2 (Ubuntu).

## Capabilities (target)

- 2D/3D LiDAR scanning
- Depth camera (RGB-D) perception
- Wheel/IMU odometry and sensor fusion
- Point cloud generation and 3D model/map output
- Live camera feed (remote viewing)
- Motor control (differential drive)

## Repository layout

This repository is a single ROS 2 package (`ament_cmake`) placed inside a colcon workspace's `src/` folder.

| Path | Contents |
|---|---|
| `description/` | URDF/xacro robot model (`robot.urdf.xacro`) |
| `launch/` | Launch files (`rsp.launch.py` = robot_state_publisher) |
| `config/` | Parameter YAML files |
| `worlds/` | Gazebo simulation worlds |
| `docs/` | Architecture, hardware, decisions, research, setup |
| `CLAUDE.md` | Project context for Claude Code |

## Quick start

```bash
mkdir -p ~/rover_ws/src && cd ~/rover_ws/src
git clone https://github.com/AMJuan1/Rover_2.git
cd ~/rover_ws
source /opt/ros/$ROS_DISTRO/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch Rover_2 rsp.launch.py
```

See `docs/setup.md` for full machine setup.

## Documentation

- [Architecture](docs/architecture.md)
- [Hardware](docs/hardware.md)
- [Decisions log](docs/decisions.md)
- [Setup](docs/setup.md)
- [Research notes](docs/research/)
- [Hand-off log (Claude Code ⇄ Claude app)](docs/handoff.md)
