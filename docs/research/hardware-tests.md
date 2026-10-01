# Hardware evaluation tests

Phase defined by ADR-005: test each new device standalone on the dev machine before it is integrated into the rover.

## Devices

| Device | Model | Interface | ROS 2 Humble driver | Status |
|---|---|---|---|---|
| LiDAR (new) | Livox Mid-360 | Ethernet 100BASE-TX (PTPv2 sync), built-in IMU | `livox_ros_driver2` | Not started |
| Depth camera (new) | Intel RealSense D435i | USB 3, built-in IMU | `realsense2_camera` (realsense-ros) | Not started |
| Gimbal camera | Not purchased yet (candidate: SIYI A8 mini) | Ethernet (video + control SDK) | Community SIYI ROS SDKs, to be evaluated | Selection pending: pipe diameter and mapping role |

## Standard test sequence (per device)

| # | Test | Command / method | Pass criterion |
|---|---|---|---|
| 1 | Detected by OS | `lsusb`, `dmesg -w`, `ls /dev/ttyUSB* /dev/video*`, `ip a` (Ethernet LiDAR) | Device enumerates with expected ID |
| 2 | Vendor tool (if any) | Vendor SDK/viewer, terminal only where possible | Raw data visible |
| 3 | ROS 2 driver launch | Driver's launch file with a config in `tests/<device>/` | Node starts without errors |
| 4 | Topics and rates | `ros2 topic list`, `ros2 topic hz <topic>`, `ros2 topic bw <topic>` | Rate matches spec |
| 5 | Data quality | Visualize (RViz2 / Foxglove); check range, noise, dropouts | Documented observations |
| 6 | Frames | `ros2 run tf2_tools view_frames` | Frame IDs correct (REP-103/105) |
| 7 | Load | `top` / `htop` while streaming | CPU/USB bandwidth acceptable |
| 8 | Recording | `ros2 bag record` short sample (kept out of git) | Bag plays back correctly |
| 9 | Raspberry Pi 4 load | Run Mid-360 + D435i drivers and recording on the Pi 4 simultaneously | No dropped messages; CPU headroom documented |

## Results

Add one section per device with: date, model, firmware, driver version, test results (table above), issues, and a verdict (adopt / reject / needs more testing).

### Livox Mid-360 — 2026-09-30 (Claude Code, dev laptop)
| Item | Value |
|---|---|
| Serial | 47MDM7F0020251 |
| IP | 192.168.1.151/24, gw 192.168.1.1 (factory default) |
| MAC | e4:7a:2c:c2:c1:5f |
| Firmware | App 13.18.2.21 (build 2023-12-19), loader 13.17.99.20. Latest published: 13.18.0244 (2025-04-11) |
| Factory config | pcl_data_type 1 (32-bit Cartesian), pattern_mode 0, full FOV (−7° to 52°); points → 192.168.1.5:56301, IMU → 192.168.1.5:56401, status push → broadcast:56201 |
| Power | 12 V bench supply |
| Host link | Realtek RTL8153 USB-Ethernet via Anker USB-C hub; NetworkManager profile `livox-mid360`, static 192.168.1.50/24 + 192.168.1.5/24 |

| # | Test | Result |
|---|---|---|
| 1 | Detected by OS | PASS: link up; ping 1.7 ms avg, 0 % loss |
| 2 | Vendor tool / raw data | PASS: status push decoded (work_state 01 = sampling, core temp 33.6 °C, HMS 01). Point stream **200 026 pts/s** (2084 pkt/s, 96 pts/pkt, 23 Mbit/s); IMU **200 Hz**. Livox Viewer 2: clean point cloud (Jan, visual); sample recording `2026-09-30_12-30-50.lvx2` (21 MB, kept out of git) |
| 3 | ROS 2 driver launch | PASS (2026-10-01): livox_ros_driver2 1.2.8, `tests/mid360/mid360.launch.py`, "Init lds lidar success" |
| 4 | Topics and rates | PASS: `/livox/lidar` 10.00 Hz, 19 968 pts/frame, 5.2 MB/s (PointCloud2, xfer_format 0); `/livox/imu` 200.0 Hz. Frame `livox_frame` |
| 7 | Load (dev laptop) | Driver ~8 % of one core (Ryzen 9 5900HS) |
| 5, 6, 8 | Quality in RViz, frames, rosbag | Pending |
| 9 | Pi 4 load | Not started |

Notes:
- The sensor ships sending data to `192.168.1.5` (SDK default), not `192.168.1.50` (manual). Giving the host both addresses avoids reconfiguring the sensor.
- 23 Mbit/s raw point stream confirms the tethered-Ethernet budget in ADR-006 (100BASE-TX is sufficient for one Mid-360).

### Intel RealSense D435 — 2026-10-01 (Claude Code, dev laptop)
**The unit is a D435 (USB PID 0x0B07), not a D435i: it has no IMU.** Docs that assume a D435i IMU (ADR-006, `pipe-inspection-sensing.md`) need review.

| Item | Value |
|---|---|
| Serial | 317222072008 |
| Firmware | 5.13.0.55 (SDK 2.58.4 recommends ≥ 5.17.3.10) |
| SDK | librealsense2-utils 2.58.4 (apt, no DKMS; kernel 6.8.0-85) |
| Link | USB 3.2 descriptor, direct laptop port (bus 002) |

| # | Test | Result |
|---|---|---|
| 1 | Detected by OS | PASS: `8086:0b07`, `/dev/video0–5`, USB 3 |
| 2 | Vendor tool / raw data | PASS (rates, 10 s each via `rs-data-collect`): depth 848×480 + RGB 1280×720 @30 → 29.6 / 30.1 fps; depth 1280×720 + RGB 1920×1080 @30 → 28.8 / 29.2 fps; depth + IR 848×480 @90 → 89.9 / 89.9 fps. One 190–290 ms gap per run in depth at 30 fps (start-up, to confirm). `realsense-viewer` visual check pending Jan |
| 3 | ROS 2 driver launch | PASS: `realsense2_camera` 4.58.4, "RealSense Node Is Up", FW 5.17.3.10 (updated by realsense-viewer) |
| 4 | Topics and rates | depth 29.98 Hz (24 MB/s), aligned depth 29.81 Hz (55 MB/s), point cloud 29.71 Hz (112 MB/s, ~186 k pts), color **16.0 Hz** in one run vs 29.98 Hz in an earlier run — suspected RGB auto-exposure priority in low light (to confirm) |
| 7 | Load (dev laptop) | Driver ~42 % of one core with point cloud + aligned depth enabled. Expect this to be the limiting load on the Pi 4 (test 9) |
| 5, 6, 8 | Data quality, frames, recording | Pending (camera_link → camera_color_optical_frame TF present) |

Combined run (both drivers, 2026-10-01): lidar 10.00 Hz, IMU 200.0 Hz, color 29.99 Hz, depth 29.70 Hz, point cloud 30.00 Hz — no drops. Color at 30 Hz in normal light supports the auto-exposure explanation for the earlier 16 Hz.
| 9 | Pi 4 load | Not started |
