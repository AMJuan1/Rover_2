# Decisions log (ADR)

Record each design decision before implementing it. Newest at the bottom.

## Template

```
## ADR-NNN: <title>
- Date: YYYY-MM-DD
- Status: Proposed | Accepted | Superseded by ADR-NNN
- Context: <problem and constraints>
- Options: <A / B / C with key trade-offs>
- Decision: <chosen option>
- Consequences: <what changes, what to watch>
```

---

## ADR-001: Repository and workflow structure
- Date: 2026-09-28
- Status: Accepted
- Context: Project combines hardware-bound ROS 2 development with research and documentation.
- Options: (A) single tool for everything; (B) Claude Code on the Ubuntu machine for code + Claude web/app for research and docs, sharing this repository.
- Decision: B. This repository is the single source of truth; decisions and research are recorded in `docs/`.
- Consequences: Every research conclusion must be committed to `docs/` so Claude Code sees it.

## ADR-002: Visualization tooling
- Date: 2026-09-28
- Status: Proposed
- Context: RViz currently used for testing and visualization; evaluating more professional alternatives.
- Options: TODO (e.g., RViz2, Foxglove, others — research in `docs/research/visualization.md`)
- Decision: Pending.
- Consequences: Pending.

## ADR-003: Keep single-package template layout
- Date: 2026-09-28
- Status: Accepted
- Context: Repository was created from a single-package ROS 2 robot template (`description/`, `launch/`, `config/`, `worlds/` at the root).
- Options: (A) keep single package; (B) restructure into multiple packages now.
- Decision: A. Split into separate packages only when a subsystem justifies it, with its own ADR.
- Consequences: New directories must be registered in `CMakeLists.txt` `install(DIRECTORY ...)`.

## ADR-004: Rename package `Rover_2` → `rover_2`
- Date: 2026-09-29
- Status: Accepted (approved by Jan)
- Context: ROS 2 package names must be lowercase (REP-144); `Rover_2` produces warnings and breaks tooling conventions.
- Options: (A) keep `Rover_2`; (B) rename to `rover_2` now, before code is added.
- Decision: B. The GitHub repository name stays `Rover_2`; only the ROS 2 package name changes.
- Consequences: Update `package.xml`, `CMakeLists.txt` `project()`, `launch/rsp.launch.py` (`get_package_share_directory`), `CLAUDE.md` and docs commands (`--packages-select rover_2`, `ros2 launch rover_2 ...`).

## ADR-005: Current phase is hardware evaluation, not rover integration
- Date: 2026-09-29
- Status: Accepted (Jan)
- Context: Jan has a new LiDAR and a new depth camera, and plans to acquire a gimbal camera. He wants to learn how each device works before committing to the rover build.
- Options: (A) start the roadmap (URDF, motor control); (B) evaluate each device standalone first.
- Decision: B. Roadmap steps 1–7 in `CLAUDE.md` are on hold. Detailed rover hardware data (dimensions, mounting, wiring) is not collected in this phase.
- Consequences: Work is organized per device under `tests/` and documented in `docs/research/hardware-tests.md`. Test launch files and configs stay outside the rover's main launch tree until a device is adopted (each adoption gets its own ADR).

## ADR-006: Sensing and compute architecture for pipe inspection
- Date: 2026-09-29
- Status: Proposed (pending hardware tests)
- Context: Dry concrete pipes 22–35 in, runs usually < 100 m, tethered Ethernet, Raspberry Pi 4 on board. Deliverables: live video + live distance/map; offline blueprint (length, direction, slope) and textured 3D model. See `docs/research/pipe-inspection-sensing.md`.
- Options: (A) gimbal camera used for both inspection and model texture; (B) fixed, calibrated sensors for mapping and texture, gimbal only for operator inspection.
- Decision: B (proposed). Mid-360 = geometry + localization; D435i (or a later fixed camera) = texture + close-range depth; gimbal = live inspection. Localization = LiDAR-inertial SLAM fused with wheel odometry and IMU. Pi 4 runs drivers, motor control and recording to SSD; live SLAM runs on the operator laptop over the tether; heavy processing is offline.
- Consequences: On-board Ethernet switch and USB 3 SSD required. Camera–LiDAR calibration and time sync required. Blueprint needs georeferencing at the entry manhole (GNSS position + initial heading). Pi 4 load must be verified; upgrade path is Pi 5 or Jetson Orin Nano.

## ADR-007: ROS 2 sensor drivers for the hardware-evaluation phase
- Date: 2026-10-01
- Status: Accepted (Jan: "set up ROS and integrate the two sensors")
- Context: Mid-360 and D435 passed vendor-tool tests; ROS 2 Humble installed on the dev laptop.
- Options: (A) vendor drivers as-is, launched from standalone test launch files; (B) wrap them in the `rover_2` package now.
- Decision: A. `livox_ros_driver2` built from source in `~/rover_ws/src/` (not vendored in this repo; Livox-SDK2 installed to `/usr/local`). `realsense2_camera` 4.58.4 from apt (`ros-humble-realsense2-camera`). Test launch files and configs live in `tests/mid360/` and `tests/d435/` and are run by path (`ros2 launch <path>`).
- Consequences: Integration into `rover_2` launch tree, URDF frames and `config/` comes with the rover build (roadmap), via a later ADR. Driver sources must be re-fetched on a new machine (see `tests/*/README.md`).
