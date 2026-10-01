# V1 reference: Articulated Robotics "Mobile Robot" series (articubot_one)
- Date: 2026-10-01
- Status: Read in full by the app (13 pages + source code of the three repositories). Jan's v1 rover and control PCB follow this series; the `Rover_2` repo was created from its `my_bot` template.
- Sources: https://articulatedrobotics.xyz/tutorials/mobile-robot/project-overview · https://github.com/joshnewans/articubot_one · https://github.com/joshnewans/ros_arduino_bridge · https://github.com/joshnewans/diffdrive_arduino (branch `humble`)

## Series content
| Part | Page | Key content |
|---|---|---|
| Concept | URDF | `robot.urdf.xacro` → `robot_core.xacro` + `inertial_macros.xacro`; `base_link` at drive-axle center; wheels on continuous joints; caster sphere |
| Concept | Gazebo | `launch_sim.launch.py`; DiffDrive plugin, then ros2_control; sphere wheel collisions; zero-friction caster; `gz_bridge.yaml` |
| Hardware | Raspberry Pi | Pi 4/5, Ubuntu + matching ROS distro, SSH, workspace cloned from GitHub, powered USB hub |
| Hardware | Power | 3S LiPo; 12 V motors; 5 V buck (25 W) for logic; 5 V budget ≈ 5 A, motors 3.6 A stall; fuse + main switch; XT60 |
| Hardware | Lidar | RPLIDAR A1 (2D, 0.3–12 m), `rplidar_ros`, `laser_frame`, `/dev/serial/by-id` |
| Hardware | Camera | `usb_cam` or `camera_ros`; `camera_link` + `camera_link_optical`; compressed image transport over the network |
| Applications | ros2_control concepts / extra / real | Controller manager, `diff_drive_controller` (`diff_cont`), `joint_state_broadcaster` (`joint_broad`); `sim_mode` xacro switch; real robot via `diffdrive_arduino` |
| Applications | Teleop | `joy` + `teleop_twist_joy` (dead-man enable button, turbo), `twist_mux` priorities (joystick 100 > tracker 20 > navigation 10) |
| Applications | SLAM | `slam_toolbox` online async, 2D grid map, `base_footprint`, serialize/localize |
| Applications | Nav2 | `nav2_bringup`, costmaps, AMCL |
| Applications | Object tracking | OpenCV ball tracker → `cmd_vel_tracker` |

## Low-level control chain (what v1 actually runs)
```
/cmd_vel (twist_mux) → diff_drive_controller → diffdrive_arduino (ros2_control SystemInterface, libserial)
   → USB serial 57600 baud → Arduino Nano (ROSArduinoBridge) → L298N → 2 motors; encoders → Nano ISRs
```

### Arduino firmware (`ros_arduino_bridge`, fork of hbrobotics)
| Item | Value |
|---|---|
| Protocol | ASCII, one command per line ending in `\r`; replies end in `\r\n` |
| Commands | `e` → `"<left> <right>"` encoder counts · `r` reset encoders · `m <l> <r>` closed-loop speed in **counts per PID loop** · `o <l> <r>` raw PWM −255…255 · `u Kp:Kd:Ki:Ko` PID update · `a <pin>` analog read · `d`/`x`/`c` digital read/write/pinMode · `b` baud |
| Rates | 57600 baud; PID at **30 Hz**; auto-stop after **2 s** without a motor command |
| PID | Integer, incremental form; defaults Kp 20, Kd 12, Ki 0, Ko 50; output clamped ±255 |
| Motor driver | `L298_MOTOR_DRIVER`: RIGHT_BACKWARD D5, LEFT_BACKWARD D6, RIGHT_FORWARD D9, LEFT_FORWARD D10 (enables D12/D13) |
| Encoders | `ARDUINO_ENC_COUNTER`: left D2/D3 (PORTD, PCINT2), right A4/A5 (PORTC, PCINT1); 4× quadrature via 16-entry lookup table |

**Jan's PCB matches this firmware pin-for-pin** (IN1 D6, IN2 D10, IN3 D9, IN4 D5; encoders D2/D3, A4/A5; enables tied high instead of D12/D13), so the firmware runs unmodified on it.

### ROS 2 hardware interface (`diffdrive_arduino`, humble branch)
- `SystemInterface` plugin with **2 joints**, each: command `velocity`, states `position` + `velocity`.
- Parameters: `left_wheel_name`, `right_wheel_name`, `loop_rate`, `device`, `baud_rate`, `timeout_ms`, `enc_counts_per_rev`, optional `pid_p/d/i/o` (sent with `u` on activate).
- `read()`: sends `e`, converts counts → rad (`2π / enc_counts_per_rev`), velocity = Δposition / period.
- `write()`: rad/s → counts per loop (`cmd / rads_per_count / loop_rate`) → sends `m l r`.
- Synchronous request/response every controller cycle (30 Hz in articubot `my_controllers.yaml`).
- articubot values: `wheel_separation` 0.297, `wheel_radius` 0.033, `enc_counts_per_rev` 3436, `/dev/ttyUSB0`.

## What carries over to Rover V2 and what does not
| Area | V1 (articubot) | V2 implication |
|---|---|---|
| Package layout, URDF style, launch structure | ✔ | Already reused (`Rover_2` from `my_bot` template) |
| Nano + ASCII serial + ros2_control hardware interface | ✔ | Good base; extend from 2 to **4 motor channels** (front motors have no encoders) |
| `diff_drive_controller` | 2 wheels | Works for skid steer with `wheels_per_side` / multiple wheel names; wheel odometry low-weight |
| L298N, both motors of a side in parallel | ✔ | Replace (see `pcb-review.md`) |
| `twist_mux` + `teleop_twist_joy` dead-man switch | ✔ | Reuse as-is for pipe teleop |
| Camera via `usb_cam` + compressed transport | ✔ | Reuse for the Arducam (MJPEG) |
| 2D RPLIDAR + `slam_toolbox` | ✔ | **Not applicable**: Mid-360 3D in a pipe → LiDAR-inertial odometry (e.g. FAST-LIO2) on the laptop |
| Nav2 / AMCL / ball tracker | ✔ | Not needed (teleoperated inspection) |
| Wi-Fi networking | ✔ | Tethered Ethernet; same ROS distro on Pi and laptop (Humble) |
| Power concept (3S, buck, fuse, switch) | ✔ | Same concept; larger 5 V budget and separate servo/LED rail |
