# CLAUDE.md — Rover project context

## Project
ROS 2 differential-drive rover with LiDAR, depth camera, odometry, point cloud / 3D model generation, and live camera feed. Owner: Jan (mechatronics engineer).

## Environment
- OS: Ubuntu <VERSION — TODO>
- ROS 2 distro: <DISTRO — TODO> (22.04 → Humble, 24.04 → Jazzy)
- Workspace: `~/rover_ws/` with this repo cloned at `~/rover_ws/src/Rover_2/`
- Build: `cd ~/rover_ws && colcon build --symlink-install`
- Source after build: `source ~/rover_ws/install/setup.bash`

## Hardware (details in docs/hardware.md)
- LiDAR: <MODEL — TODO>
- Depth camera: <MODEL — TODO>
- Motor driver / controller: <MODEL — TODO>
- Compute: <BOARD/PC — TODO>
- IMU: <MODEL or none — TODO>

## Current layout (single package `Rover_2`, ament_cmake, at repo root)
| Path | Purpose |
|---|---|
| `description/robot.urdf.xacro` | Robot model (URDF/xacro) |
| `launch/rsp.launch.py` | robot_state_publisher launch |
| `config/` | Parameter YAMLs |
| `worlds/` | Gazebo worlds |
| `docs/` | Architecture, hardware, decisions, research |

New directories must be added to the `install(DIRECTORY ...)` list in `CMakeLists.txt`.

## Planned subsystems (split into separate packages only when justified; record an ADR first)
| Subsystem | Purpose |
|---|---|
| hardware | Motor control, encoders, ros2_control interface |
| sensors | LiDAR, depth camera, IMU driver launch/config |
| localization | EKF (robot_localization), odometry fusion |
| mapping | SLAM, point cloud processing, 3D model export |
| streaming | Live camera feed to remote clients |

Create any new package with `ros2 pkg create`, never by hand.

## Conventions
- Follow REP-103 (units, axes) and REP-105 (frames: map → odom → base_link).
- All tunable values go in YAML under `config/`, not hardcoded.
- One launch file per subsystem; a top-level `launch/rover.launch.py` includes them.
- Record every design decision in `docs/decisions.md` (ADR format) before implementing it.
- Research findings go in `docs/research/`, one file per topic.
- Commit messages: `<area>: <imperative summary>` (e.g. `launch: add lidar launch`).

## Workflow rules
- Build and test after every change: `colcon build --packages-select Rover_2 && colcon test --packages-select Rover_2`.
- Verify against live data when hardware is connected (`ros2 topic list`, `ros2 topic hz`, `ros2 run tf2_tools view_frames`).
- Do not change motor-control parameters (speed limits, PID gains) without stating the old and new values.
- Terminal commands only; no GUI steps.
