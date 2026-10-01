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
