# Architecture

## Frames (REP-105)

```
map ──> odom ──> base_link ──┬──> laser_frame
                             ├──> camera_link ──> camera_depth_optical_frame
                             └──> imu_link
```

| Transform | Published by |
|---|---|
| map → odom | SLAM node (mapping) |
| odom → base_link | EKF (localization) |
| base_link → sensors | robot_state_publisher (`launch/rsp.launch.py`) |

## Data flow

```
Encoders ──> hardware ──> /wheel/odometry ─┐
IMU ───────> sensors ───> /imu/data ───────┴──> EKF ──> /odometry/filtered
LiDAR ─────> sensors ───> /scan ──────────────> SLAM ──> /map
Depth cam ─> sensors ───> /camera/depth/points ──> mapping ──> point cloud / 3D model
RGB cam ───> sensors ───> /camera/color/image_raw ──> streaming ──> remote viewer
/cmd_vel ──> hardware ──> motor driver
```

## Key topics

| Topic | Type | Source |
|---|---|---|
| `/cmd_vel` | geometry_msgs/Twist | teleop / navigation |
| `/wheel/odometry` | nav_msgs/Odometry | hardware |
| `/imu/data` | sensor_msgs/Imu | sensors |
| `/scan` | sensor_msgs/LaserScan | sensors |
| `/camera/depth/points` | sensor_msgs/PointCloud2 | sensors |
| `/camera/color/image_raw` | sensor_msgs/Image | sensors |
| `/odometry/filtered` | nav_msgs/Odometry | localization |
| `/map` | nav_msgs/OccupancyGrid | mapping |

Topic names are provisional; update this table when drivers are integrated.
