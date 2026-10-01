# Architecture

## Frames (REP-105)

```
map ──> odom ──> base_footprint ──> base_link (rear axle center) ──┬──> 4 wheel links
                                                                  ├──> livox_frame (Mid-360 point-cloud origin, pitched −45°; IMU data in this frame)
                                                                  └──> camera_link (D435 depth origin) ──> optical frames (published by realsense2_camera)
```

Sensor poses: `config/sensor_poses.yaml` (CAD prior from drawing v6, to be replaced by calibration). URDF: `description/robot.urdf.xacro`.

| Transform | Published by |
|---|---|
| map → odom | SLAM node (mapping) |
| odom → base_footprint | EKF / LiDAR-inertial odometry (localization) |
| base_footprint → base_link → sensors | robot_state_publisher (`launch/rsp.launch.py`) |

## Data flow (ADR-006)

```
Rear encoders ─> hardware (Pi 4) ─> /wheel/odometry ─┐
Mid-360 IMU ───> /livox/imu ─────────────────────────┼─> LiDAR-inertial odometry + wheel odometry (laptop) ─> pose, distance travelled
Mid-360 ───────> /livox/lidar ─> body crop box ──────┘                                               └─> live map (Foxglove/RViz)
D435 ──────────> raw depth + color ─> recorded on Pi 4 SSD ─> offline: colored cloud / textured model / blueprint
Gimbal camera ─> own encoded stream ─> switch ─> tether ─> operator laptop (live inspection)
/cmd_vel ──────> hardware ─> motor drivers
```

## Key topics

| Topic | Type | Source |
|---|---|---|
| `/cmd_vel` | geometry_msgs/Twist | teleop / navigation |
| `/wheel/odometry` | nav_msgs/Odometry | hardware |
| `/livox/imu` | sensor_msgs/Imu (200 Hz, Mid-360 built-in; only IMU) | sensors |
| `/livox/lidar` | sensor_msgs/PointCloud2 (10 Hz, `livox_frame`) | sensors |
| `/camera/camera/depth/image_rect_raw` | sensor_msgs/Image (D435) | sensors |
| `/camera/camera/color/image_raw` | sensor_msgs/Image (D435) | sensors |
| `/odometry/filtered` | nav_msgs/Odometry | localization |
| `/map` | nav_msgs/OccupancyGrid | mapping |

Topic names are provisional; update this table when drivers are integrated.
