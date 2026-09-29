# Hardware

## Bill of materials

| Component | Model | Interface | ROS 2 driver | Status |
|---|---|---|---|---|
| Compute | TODO | — | — | TODO |
| LiDAR | TODO | USB / Ethernet | TODO | TODO |
| Depth camera | TODO | USB 3 | TODO | TODO |
| IMU | TODO | I2C / USB | TODO | TODO |
| Motor driver | TODO | Serial / PWM / CAN | TODO | TODO |
| Motors + encoders | TODO | — | — | TODO |
| Battery / power | TODO | — | — | TODO |

## Physical dimensions (for URDF)

| Parameter | Value | Unit |
|---|---|---|
| Wheel radius | TODO | m |
| Wheel separation (track) | TODO | m |
| Encoder ticks per revolution | TODO | ticks |
| Gear ratio | TODO | — |
| base_link → LiDAR (x, y, z, roll, pitch, yaw) | TODO | m, rad |
| base_link → camera (x, y, z, roll, pitch, yaw) | TODO | m, rad |
| base_link → IMU (x, y, z, roll, pitch, yaw) | TODO | m, rad |

## Wiring

TODO: power distribution and signal wiring diagram.

## Device paths (udev)

| Device | Symlink | udev rule |
|---|---|---|
| LiDAR | `/dev/rover_lidar` | TODO |
| Motor controller | `/dev/rover_motors` | TODO |
