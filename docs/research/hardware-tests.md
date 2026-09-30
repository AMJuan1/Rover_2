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
| 2 | Vendor tool / raw data | PASS (raw): status push decoded (work_state 01 = sampling, core temp 33.6 °C, HMS 01). Point stream **200 026 pts/s** (2084 pkt/s, 96 pts/pkt, 23 Mbit/s); IMU **200 Hz**. Livox Viewer 2 v2.3.0 launched — visual check pending Jan |
| 3–8 | ROS 2 driver tests | Deferred (ROS 2 Humble not installed) |
| 9 | Pi 4 load | Not started |

Notes:
- The sensor ships sending data to `192.168.1.5` (SDK default), not `192.168.1.50` (manual). Giving the host both addresses avoids reconfiguring the sensor.
- 23 Mbit/s raw point stream confirms the tethered-Ethernet budget in ADR-006 (100BASE-TX is sufficient for one Mid-360).
