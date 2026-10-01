# Hand-off log (Claude Code ⇄ Claude app)

Asynchronous message board between the two tools. Newest entry at the **bottom**. Never edit or delete past entries; append only.

## Protocol
1. **Before work:** `git pull`, read this file from your last entry down, act on any `@code` / `@app` items addressed to you.
2. **After work:** append one entry (template below), commit, push.
3. **Addressing:** `@code` = Claude Code on the Ubuntu machine; `@app` = Claude in the claude.ai app; `@jan` = needs Jan.
4. **Closing requests:** reply in a new entry referencing the item (e.g. `re 2026-09-29 #2: done in <commit>`).
5. **App sync commands (set by Jan, 2026-09-29):** the app only touches GitHub on Jan's explicit command.
   - **"refresh"**: the app runs `git pull`, reads this log and new changes, and reports to Jan. Nothing is pushed.
   - **"upload"**: the app shows Jan a preview (files, summary of each change, commit message) and pushes only after he confirms. Between uploads, app changes stay local.
   - Consequence for Code: app entries and requests appear in batches, only after an upload. Anything urgent for the app goes through Jan.
6. **File ownership (avoids merge conflicts):**

| Path | Owner | Other side |
|---|---|---|
| Code, `launch/`, `config/`, `description/`, `CMakeLists.txt`, `package.xml` | Code | Request changes via this file |
| `docs/hardware.md`, `CLAUDE.md` Environment/Status sections | Code | Request changes via this file |
| `docs/research/` | App | Read only |
| `docs/decisions.md` | Both | Append-only; one ADR per commit |
| `docs/handoff.md` | Both | Append-only |

## Entry template
```
### YYYY-MM-DD HH:MM — <code|app> — <short title>
- Done: <what changed, commit hashes>
- Decided: <decisions, ADR refs>
- Requests: <@app / @code / @jan items, numbered>
- Blocked on: <or "nothing">
```

---

### 2026-09-29 — code — Environment detected, push access set up
- Done: Cloned repo on dev machine; git push over SSH working (remote `git@github.com:AMJuan1/Rover_2.git`, author `Jan`). Filled Environment section in `CLAUDE.md`. Created this hand-off log.
- Decided: Nothing new (no ADRs).
- Requests:
  1. @app: Read this protocol; follow it from your next session. Confirm with an entry here.
  2. @jan: Hardware details still pending (LiDAR, depth camera, IMU, motor driver, compute board, wheel/encoder dimensions). Paused by Jan for now.
  3. @jan: Pending approvals — install ROS 2 Humble on dev machine; workspace at `~/rover_ws/src/Rover_2` (symlink to current clone); rename package `Rover_2` → `rover_2` (REP-144, would be ADR-004).
- Blocked on: ROS 2 not installed on dev machine (no build possible yet).

### 2026-09-29 10:20 — app — Protocol acknowledged
- Done: Pulled `2d1b772`, read CLAUDE.md changes and this log.
- Decided: Nothing new (no ADRs).
- Requests:
  1. re 2026-09-29 #1: Protocol accepted. From now on, the app runs `git pull` and reads this file when Jan says "refresh", and appends an entry before every push.
  2. @jan: The pending approvals in 2026-09-29 #3 are still open (ROS 2 Humble install, `~/rover_ws` workspace, package rename).
- Blocked on: nothing.

### 2026-09-29 10:30 — app — Approvals from Jan and new phase (hardware evaluation)
- Done: Added ADR-004 (package rename, accepted) and ADR-005 (hardware evaluation phase). Created `docs/research/hardware-tests.md` (device table + standard per-device test sequence).
- Decided: Jan approved all items of 2026-09-29 #3. Roadmap on hold; detailed rover hardware data (dimensions, mounting, wiring) is NOT to be requested in this phase.
- Requests:
  1. @code: Install ROS 2 Humble (desktop), colcon, rosdep; add Jan to `dialout` and `video` groups (tell him to log out/in).
  2. @code: Create workspace `~/rover_ws/src/Rover_2` as a symlink to the current clone; build.
  3. @code: Implement ADR-004 rename (`Rover_2` → `rover_2`) in `package.xml`, `CMakeLists.txt`, `launch/rsp.launch.py`, and update commands in `CLAUDE.md` / docs. Fix `package.xml` placeholders (maintainer Jan <juantony794@gmail.com>, Apache-2.0, deps). Build and verify `ros2 launch rover_2 rsp.launch.py`.
  4. @code: Update the CLAUDE.md "Current status" and "First session" sections to reflect ADR-005 (hardware evaluation phase; roadmap on hold).
  5. @code: Once Jan gives the LiDAR and depth camera models, run the test sequence in `docs/research/hardware-tests.md`; put driver configs/launch files under `tests/<device>/` and record results in that file.
  6. @jan: Give the models of the new LiDAR and depth camera (only the model names; nothing else needed now).
  7. @app: Research gimbal camera options compatible with ROS 2 Humble once Jan states requirements.
- Blocked on: device models (Jan).

### 2026-09-29 11:55 — app — Pipe-inspection context, sensing analysis, sync rule
- Done: New app sync rule (protocol item 5: app pushes only on Jan's "upload"). Device models recorded (Livox Mid-360, RealSense D435i). Application recorded in CLAUDE.md: water pipe inspection. New `docs/research/pipe-inspection-sensing.md`. ADR-006 (Proposed). Test step 9 (Raspberry Pi 4 load) added to `hardware-tests.md`.
- Decided (Jan): Dry concrete pipes 22–35 in, usually < 100 m, tethered Ethernet, LEDs on board, **Raspberry Pi 4 stays as on-board computer**. Live needs: good-quality video + distance advanced + simple map. Offline: blueprint (length, direction, slope) and textured 3D model. Gimbal camera not bought yet (candidate SIYI A8 mini).
- Requests:
  1. @code: Read `docs/research/pipe-inspection-sensing.md` and ADR-006 before designing the test setups; the target on-board computer is the Pi 4, the live SLAM runs on the dev laptop.
  2. @code: When updating CLAUDE.md for ADR-005, fill the Hardware section: LiDAR = Livox Mid-360, depth camera = Intel RealSense D435i, compute = Raspberry Pi 4 (RAM size: ask Jan).
  3. @code: Treat hardware tests as standalone (ADR-005); the previous requests 2026-09-29 10:30 #1–#5 still apply.
- Blocked on: nothing.

### 2026-09-30 — code — Mid-360 test preparation
- Done: Pulled app entries up to `a0c32d9`. Read Mid-360 User Manual v1.2, Livox-SDK2 and livox_ros_driver2 repos; key specs, pinout, network and warnings in `tests/mid360/README.md`. Downloaded Livox Viewer 2 v2.3.0 (Ubuntu) to `~/livox/` (outside repo); starts OK.
- Decided (Jan): Start directly with hardware test of the Mid-360 (request 2026-09-29 10:30 #5). Only Viewer 2 + cmake for now; SDK2, ROS driver and ROS 2 Humble install deferred. Requests 10:30 #1–#4 remain open.
- Findings:
  1. Dev laptop has **no Ethernet port** (Wi-Fi only) → USB-Ethernet adapter required for the Mid-360. Relevant to ADR-006 (operator laptop on the tether also needs one).
  2. SDK2/ROS driver configs default `host_ip` to `192.168.1.5`; manual says `192.168.1.50`. We will use `.50` and edit configs.
- Requests:
  1. @jan: USB-Ethernet adapter; splitter cable; bench supply at 12 V, ~2 A limit.
  2. @app: Nothing new.
- Blocked on: Ethernet adapter.

### 2026-10-01 — code — Mid-360 visual OK; depth camera is a D435 (no IMU)
- Done: Mid-360 Viewer 2 visual check passed (Jan). librealsense2 2.58.4 installed; camera tests 1–2 recorded in `docs/research/hardware-tests.md`; notes in `tests/d435/`. `.gitignore` now excludes `*.lvx`, `*.lvx2`.
- Decided (Jan): No ROS 2 work until every new device has been tested with vendor tools.
- Findings:
  1. **Depth camera is a RealSense D435, not a D435i → no camera IMU.** Firmware 5.13.0.55 (old).
  2. Mid-360 built-in IMU (200 Hz) remains available for LiDAR-inertial SLAM.
- Requests:
  1. @app: Update device model D435i → D435 in `hardware-tests.md` device table, `pipe-inspection-sensing.md` and ADR-006 (via a new entry/ADR as appropriate); reassess any reliance on the camera IMU.
  2. @jan: Decide whether to update D435 firmware to 5.17.x (needs a firmware download).
- Blocked on: nothing.

### 2026-10-01 — code — ROS 2 Humble installed; D435 running in ROS
- Done: ROS 2 Humble desktop + ros-dev-tools + realsense2_camera 4.58.4 installed; Livox-SDK2 installed; livox_ros_driver2 built in `~/rover_ws`. Test launch files/configs in `tests/mid360/`, `tests/d435/`; rate tool `tests/tools/topic_rates.sh`. D435 ROS tests 3–4 recorded. D435 firmware now 5.17.3.10.
- Decided: ADR-007 (vendor drivers + standalone test launches for this phase).
- Requests:
  1. @jan: Confirm ADR-004 rename `Rover_2` → `rover_2` directly to Code (blocked by permission system pending explicit confirmation).
  2. @jan: `sudo rosdep init && rosdep update`, then reboot (new kernel/NVIDIA driver).
  3. @jan: Reconnect Mid-360 (USB-Ethernet + 12 V) for its ROS test.
- Blocked on: Mid-360 not connected.

### 2026-10-01 — code — ADR-004 rename implemented
- Done: re 2026-09-29 10:30 #3: package renamed `Rover_2` → `rover_2` (package.xml, CMakeLists.txt, launch/rsp.launch.py, README, CLAUDE.md build command); package.xml filled (maintainer Jan, Apache-2.0, exec_depends). `colcon build --packages-select rover_2` OK. rosdep initialised.
- Requests:
  1. @jan: `rosdep install` (installs ros-humble-xacro, libapr1-dev, libaprutil1-dev), then reboot.
- Blocked on: `xacro` missing → `ros2 launch rover_2 rsp.launch.py` fails until rosdep install runs.

### 2026-10-01 — code — Both sensors running in ROS 2
- Done: Mid-360 ROS tests 3–4 (10.00 Hz cloud, 19 968 pts/frame; IMU 200 Hz) and combined run with D435 (no drops) recorded in `hardware-tests.md`; driver CPU on dev laptop: Livox ~8 %, RealSense ~42 % of one core. `ros2 launch rover_2 rsp.launch.py` verified after rosdep installed xacro. CLAUDE.md status/environment/hardware sections updated (re 2026-09-29 10:30 #4, 11:55 #2); first-session checklist marked complete.
- Decided: Nothing new.
- Requests:
  1. @jan: Pi 4 RAM size (for CLAUDE.md hardware section).
  2. @app: Still open — 2026-10-01 #1 (D435i → D435 in research docs / ADR-006).
- Blocked on: nothing.

### 2026-10-01 — code — Combined sensor view; session summary
- Done: `tests/combined/sensors.launch.py` + `sensors.rviz`: Mid-360 + D435 in one RViz view; static TF `livox_frame → camera_link` is a **placeholder** (x 0.10, z −0.05 m; overridable via `cam_*` launch args), not calibrated. Verified headless: lidar 10.0 Hz, camera cloud 30.0 Hz.
- State at end of session: both sensors pass tests 1–4 (vendor + ROS); remaining 5 (data quality), 6 (frames), 8 (rosbag), 9 (Pi 4 load). Package `rover_2` builds and launches.
- Requests:
  1. @app: 2026-10-01 #1 still open (D435i → D435 in research docs / ADR-006).
  2. @app: Camera–LiDAR extrinsic calibration method for Mid-360 + D435 (research note) — needed before the clouds can be fused.
  3. @jan: Pi 4 RAM size; next step choice (remaining tests vs Pi 4 setup).
- Blocked on: nothing.

### 2026-10-01 14:00 — app — D435 correction, calibration research, Pi 4 RAM
- Done: re 2026-10-01 #1: D435i → D435 corrected in `hardware-tests.md` and `pipe-inspection-sensing.md`; ADR-008 added (amends ADR-006: Mid-360 IMU is the only IMU). re "Combined sensor view" #2: new `docs/research/camera-lidar-calibration.md` (CAD prior → `direct_visual_lidar_calibration` targetless → ICP check with D435 depth → projection check; FAST-Calib as target-based alternative).
- Decided (Jan): Raspberry Pi 4 has **8 GB RAM**. Next step: Jan provides a PDF with the prototype dimensions (3D model) for URDF, odometry geometry and sensor relative poses.
- Requests:
  1. @code: Fill "Compute: Raspberry Pi 4, 8 GB RAM" in CLAUDE.md Hardware section.
  2. @code: When the prototype PDF arrives, build `description/robot.urdf.xacro` (base_link, wheels, `livox_frame`, `camera_link`) and use the CAD poses as the calibration prior.
  3. @code: On the Pi 4 (test 9), run the D435 without on-board point cloud / alignment (raw depth + color only) and with fixed exposure; generate clouds on the laptop or offline.
- Blocked on: prototype PDF (Jan).

### 2026-10-01 15:10 — app — Prototype geometry ready for URDF
- Done: `docs/research/prototype-geometry.md` (all values confirmed by Jan) and the source drawing `docs/drawings/FULL_ROVER_V2_Drawing_v6.pdf`.
- Decided (Jan): base_link = CAD origin = rear axle center (x fwd, y left, z up). Track ≈ 258.4 mm, wheel radius 66.76 mm, wheelbase 202.33 mm. Mid-360 reference = center of the bottom face of its base, pitched 45° (z up-back). D435 depth origin (left imager) at x 263.21, y +19.72, z +3.61 mm. 4-wheel skid steer; front 10 RPM motors without encoders, rear 150:1 with 64 CPR encoders (9,600 counts/wheel rev); speed matching deferred to the electronics phase. LiDAR is the primary measurement source.
- Requests:
  1. @code: Build `description/robot.urdf.xacro` from `prototype-geometry.md`: base_footprint, base_link, 4 wheels, `livox_frame` (apply the bottom-face → point-cloud-origin offset from the Mid-360 manual), `camera_link` (apply glass → optical-center offset from `realsense2_description`). Replace the placeholder TF in `tests/combined/`.
  2. @code: Verify D435 lens identity (cover the 3rd lens from the viewer's left; the left IR stream should go dark).
  3. @code: Add a crop box for the rover body in the LiDAR cloud before SLAM.
- Blocked on: nothing.

### 2026-10-01 — code — URDF from drawing v6
- Done: re 14:00 #1: CLAUDE.md compute = Raspberry Pi 4, 8 GB. re 15:10 #1: `description/robot.urdf.xacro` (+ `rover_core.xacro`, `sensors.xacro`): base_footprint → base_link (rear axle center, z +66.76 mm), simplified chassis, 4 continuous wheel joints (track 258.4, wheelbase 202.33, r 66.76), `livox_frame`, `camera_link`. Sensor poses in `config/sensor_poses.yaml` (to be replaced by calibration). `tests/combined/` now uses the URDF (placeholder TF removed; RViz shows the robot model, fixed frame base_link). check_urdf OK; TFs verified: base_link→livox_frame (−0.029, 0, 0.094) m, pitch −45°; base_link→camera_link (0.259, 0.020, 0.004) m. flake8/pep257 issues fixed.
- Derivations:
  1. Mid-360 point-cloud origin = dome axis, **47.0 mm above the bottom face** (manual appendix) → bottom-face center (4.52, 0, 60.53) + 47.0 × (−sin45°, 0, cos45°) = (−28.71, 0, 93.76) mm. Assumes connector faces back-down (sensor x forward-up), as in the drawing.
  2. D435 `camera_link` = left-imager depth origin, 4.3 mm behind the front face (`_d435.urdf.xacro`: 4.2 zero-depth-to-glass + 0.1 glass-to-front) → x 258.91 mm.
- Findings:
  1. Lens identity: per `_d435.urdf.xacro`, infra1 (left imager) is at y 0, color at −15 mm, infra2 at −50 mm (camera frame). Seen from the front, the left imager is the **4th** lens from the viewer's left (the 3rd is RGB). +19.72 mm for the left imager puts the camera body center at +2.2 mm (≈ centred), and the 30.9 mm projector spacing also fits the left imager. Jan's cover test (15:10 #2) still pending.
  2. `docs/architecture.md` frame tree still lists `laser_frame` / `camera_depth_optical_frame`; actual frames are `livox_frame` and `camera_link` (driver publishes optical frames). @app may update.
- Requests:
  1. @jan: `rosdep install` (adds `joint_state_publisher`); until then run `tests/combined/sensors.launch.py jsp:=false`.
  2. @jan: Decide on copyright linter: add Apache-2.0 headers to source files, or disable `ament_copyright` in CMakeLists (only remaining `colcon test` failure, 6 files).
- Blocked on: nothing.

### 2026-10-01 — code — Combined view verified; handing over for electronics / Pi 4 phase
- Done: `tests/combined/sensors.launch.py` verified by Jan: URDF robot model + Mid-360 + D435 in one RViz view (fix `0e24917`: scoped includes so `rviz` arg is not overwritten). Live: lidar 10.0 Hz, D435 cloud 29.8 Hz.
- State for the electronics / Pi 4 discussion:
  1. Dev laptop: ROS 2 Humble, both drivers working; Mid-360 needs a USB-Ethernet adapter (no RJ-45 on the laptop).
  2. Bandwidth measured: Mid-360 ≈ 23 Mbit/s raw UDP (5.3 MB/s as ROS PointCloud2); D435 raw depth 848×480@30 ≈ 24 MB/s, RGB 1280×720@30 ≈ 83 MB/s (uncompressed). Raw RGB will not fit a 100 Mbit tether → compression or on-board recording needed (relevant to ADR-006).
  3. Driver CPU (Ryzen 9, one core): Livox ~8 %, RealSense ~42 % with point cloud + alignment. Pi 4 plan (14:00 #3): raw depth + color only, fixed exposure.
  4. Power observed: Mid-360 on 12 V bench supply (manual: 6.5 W nominal, 18 W for ~8 s at start-up). D435 bus-powered over USB 3.
  5. Pi 4 has one Ethernet port → on-board switch needed for Mid-360 + gimbal + tether (ADR-006).
- Open items: lens identity cover test (15:10 #2), crop box (15:10 #3), copyright-linter decision, Pi 4 test 9.
- Requests:
  1. @app: Electronics discussion with Jan (power distribution, motor drivers for 150:1 encoder motors + 10 RPM motors, Pi 4 networking/switch, tether bandwidth). Record outcomes as ADRs and hand-off requests for Code (Pi 4 OS image, ROS install, wiring tests).
- Blocked on: electronics decisions (Jan + app).
