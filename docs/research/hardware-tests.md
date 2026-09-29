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

## Results

Add one section per device with: date, model, firmware, driver version, test results (table above), issues, and a verdict (adopt / reject / needs more testing).
