# CLAUDE.md — Rover project context

## Project
ROS 2 differential-drive rover with LiDAR, depth camera, odometry, point cloud / 3D model generation, live camera feed, and motor control. **Application: water pipe inspection** (navigation inside pipes, textured 3D model of the pipe, remote camera inspection). Owner: Jan (mechatronics engineer). GitHub: https://github.com/AMJuan1/Rover_2

## How this project is run (two tools, one repo)
- **Claude Code (you), on Jan's Ubuntu machine:** all code, builds, launches, hardware tests, live-topic debugging, motor control. You have access to the robot; the other tool does not.
- **Claude (claude.ai app):** research, long design discussions, reports, diagrams. It can read and push to this repo.
- **Communication channel:** `docs/handoff.md` — append-only log with protocol and file-ownership table. Read it after every `git pull`; append an entry before every push.
- **This repository is the single source of truth.** Anything decided in either tool must end up in `docs/` (decisions in `docs/decisions.md`, research in `docs/research/`). Before starting work, read `docs/` to pick up decisions made elsewhere. Always `git pull` before starting and push when a unit of work is done.

## Current status (as of 2026-10-01)
| Area | Status |
|---|---|
| Phase | Hardware evaluation (ADR-005); roadmap on hold. Sensor ROS drivers per ADR-007 |
| Package | Renamed `rover_2` (ADR-004); `package.xml` complete; builds; `ros2 launch rover_2 rsp.launch.py` OK |
| `description/robot.urdf.xacro` | Placeholder only (`base_link`, nothing else) |
| `config/`, `worlds/` | Empty placeholders |
| Mid-360 | Vendor + ROS tests 1–4 pass (`tests/mid360/`) |
| D435 | Vendor + ROS tests 1–4 pass (`tests/d435/`); FW 5.17.3.10 |
| Gimbal camera | Not purchased |
| Test results | `docs/research/hardware-tests.md` |
| Previous work | Jan has tested earlier versions with RViz; wants to evaluate more professional visualization tools (ADR-002, pending) |

## First session — completed 2026-10-01 (kept for setting up a new machine)
1. Detect the environment yourself: `lsb_release -a`, `echo $ROS_DISTRO`, `ls /opt/ros/`, `lsusb`, `ls /dev/tty* /dev/video*`. Fill the Environment section below with what you find.
2. Ask Jan for anything you cannot detect: LiDAR, depth camera, motor driver, compute board, IMU models; wheel radius, track width, encoder ticks, sensor mounting positions. Fill `docs/hardware.md` and the Hardware section below.
3. Fix `package.xml`: maintainer name/email (ask Jan), description, `Apache-2.0` license, missing dependencies. Run `rosdep install --from-paths src --ignore-src -r -y` from the workspace root.
4. Raise with Jan (do not act without approval): the package name `Rover_2` contains uppercase, which violates ROS 2 naming rules (REP-144) and produces warnings. Renaming to `rover_2` touches `package.xml`, `CMakeLists.txt` and `launch/rsp.launch.py`. Record the decision as an ADR.
5. Build and verify: `colcon build --symlink-install`, then `ros2 launch Rover_2 rsp.launch.py` (or the new name) and `ros2 topic list`.
6. Commit and push (`docs: fill environment and hardware details`, etc.).

## Environment
- Dev machine (detected 2026-09-29): ASUS laptop, AMD Ryzen 9 5900HS (16 threads, x86_64), 38 GiB RAM
- OS: Ubuntu 22.04.5 LTS (jammy)
- Kernel 6.8.0-138-generic; NVIDIA RTX 3060 Laptop GPU, driver 580
- ROS 2 Humble desktop + ros-dev-tools; rosdep initialised; `~/.bashrc` sources ROS and the workspace
- User groups: `video`, `plugdev` (no `dialout` yet)
- Repo cloned at `~/Documents/Claude_Projects/ROVER_V2`, symlinked as `~/rover_ws/src/Rover_2`
- Workspace: `~/rover_ws/` (also holds `livox_ros_driver2` from source)
- Mid-360 link: USB-Ethernet RTL8153 `enx6c6e071000f8`, NM profile `livox-mid360` (192.168.1.50 + 192.168.1.5)
- Vendor tools: Livox Viewer 2 in `~/livox/`; Livox-SDK2 in `/usr/local`; librealsense2 2.58.4 (apt)
- Build: `cd ~/rover_ws && colcon build --symlink-install`
- Source after build: `source ~/rover_ws/install/setup.bash`

## Hardware (details in docs/hardware.md)
- LiDAR: Livox Mid-360 (192.168.1.151; built-in 6-axis IMU)
- Depth camera: Intel RealSense D435 (**no IMU**; not a D435i)
- Motor driver / controller: <MODEL — TODO>
- Compute: Raspberry Pi 4 on board (RAM — TODO); dev/operator laptop runs SLAM
- IMU: Mid-360 built-in (no separate IMU yet)

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
- Build and test after every change: `colcon build --packages-select rover_2 && colcon test --packages-select rover_2`.
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
