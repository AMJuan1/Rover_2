# CLAUDE.md — Rover project context

## Project
ROS 2 differential-drive rover with LiDAR, depth camera, odometry, point cloud / 3D model generation, live camera feed, and motor control. Owner: Jan (mechatronics engineer). GitHub: https://github.com/AMJuan1/Rover_2

## How this project is run (two tools, one repo)
- **Claude Code (you), on Jan's Ubuntu machine:** all code, builds, launches, hardware tests, live-topic debugging, motor control. You have access to the robot; the other tool does not.
- **Claude (claude.ai app):** research, long design discussions, reports, diagrams. It can read and push to this repo.
- **This repository is the single source of truth.** Anything decided in either tool must end up in `docs/` (decisions in `docs/decisions.md`, research in `docs/research/`). Before starting work, read `docs/` to pick up decisions made elsewhere. Always `git pull` before starting and push when a unit of work is done.

## Current status (as of 2026-09-29)
| Area | Status |
|---|---|
| Repo | Created from a single-package ROS 2 robot template; docs structure added |
| `description/robot.urdf.xacro` | Placeholder only (`base_link`, nothing else) |
| `launch/rsp.launch.py` | Working robot_state_publisher launch (template) |
| `config/`, `worlds/` | Empty placeholders |
| `package.xml` | Template placeholders (maintainer, email, description); license should be `Apache-2.0` to match `LICENSE.md`; missing `exec_depend` on `robot_state_publisher`, `xacro`, `launch_ros` |
| Hardware details | Unknown — all TODO below and in `docs/hardware.md` |
| Previous work | Jan has tested earlier versions with RViz; wants to evaluate more professional visualization tools (ADR-002, pending) |

## First session — do these in order
1. Detect the environment yourself: `lsb_release -a`, `echo $ROS_DISTRO`, `ls /opt/ros/`, `lsusb`, `ls /dev/tty* /dev/video*`. Fill the Environment section below with what you find.
2. Ask Jan for anything you cannot detect: LiDAR, depth camera, motor driver, compute board, IMU models; wheel radius, track width, encoder ticks, sensor mounting positions. Fill `docs/hardware.md` and the Hardware section below.
3. Fix `package.xml`: maintainer name/email (ask Jan), description, `Apache-2.0` license, missing dependencies. Run `rosdep install --from-paths src --ignore-src -r -y` from the workspace root.
4. Raise with Jan (do not act without approval): the package name `Rover_2` contains uppercase, which violates ROS 2 naming rules (REP-144) and produces warnings. Renaming to `rover_2` touches `package.xml`, `CMakeLists.txt` and `launch/rsp.launch.py`. Record the decision as an ADR.
5. Build and verify: `colcon build --symlink-install`, then `ros2 launch Rover_2 rsp.launch.py` (or the new name) and `ros2 topic list`.
6. Commit and push (`docs: fill environment and hardware details`, etc.).

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

## Roadmap (suggested order; confirm with Jan)
1. Robot description: full URDF/xacro with real dimensions and sensor frames.
2. Motor control: ros2_control + diff_drive_controller, teleop via `/cmd_vel`, wheel odometry.
3. Sensors: LiDAR and depth camera drivers, frames verified with `view_frames`.
4. Localization: robot_localization EKF (wheel odometry + IMU).
5. Mapping: 2D SLAM from LiDAR, then point clouds / 3D model from the depth camera.
6. Live camera feed to a remote viewer.
7. Visualization tooling decision (ADR-002).

## Current layout (single package, ament_cmake, at repo root)
| Path | Purpose |
|---|---|
| `description/robot.urdf.xacro` | Robot model (URDF/xacro) |
| `launch/rsp.launch.py` | robot_state_publisher launch |
| `config/` | Parameter YAMLs |
| `worlds/` | Gazebo worlds |
| `docs/` | Architecture, hardware, decisions, research, setup |

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
- Follow REP-103 (units, axes) and REP-105 (frames: map → odom → base_link). Target architecture is in `docs/architecture.md`.
- All tunable values go in YAML under `config/`, not hardcoded.
- One launch file per subsystem; a top-level `launch/rover.launch.py` includes them.
- Record every design decision in `docs/decisions.md` (ADR format) before implementing it.
- Research findings go in `docs/research/`, one file per topic.
- Commit messages: `<area>: <imperative summary>` (e.g. `launch: add lidar launch`).
- Keep rosbags, point clouds and other large data out of git (see `.gitignore`).

## Workflow rules
- Build and test after every change: `colcon build --packages-select Rover_2 && colcon test --packages-select Rover_2`.
- Verify against live data when hardware is connected (`ros2 topic list`, `ros2 topic hz`, `ros2 run tf2_tools view_frames`).
- Do not change motor-control parameters (speed limits, PID gains) without stating the old and new values.
- Before running anything that moves the motors, tell Jan and wait for confirmation (the rover must be lifted or in a safe area).
- Ask before any change that is hard to reverse (package rename, restructuring, deleting files).

## Working with Jan
- Address him as "Sir". Formal, direct, truthful; no filler.
- Prefer structured output: tables, step-by-step terminal commands, code.
- Terminal commands only; no GUI steps.
- Iterate on his corrections without long re-explanations.
- Match the language he writes in (English or Spanish). Code, comments and docs in this repo are in English.
