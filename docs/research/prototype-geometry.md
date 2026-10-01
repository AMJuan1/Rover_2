# Prototype geometry (FULL ROVER V2 drawing v4)
- Date: 2026-10-01
- Source: `FULL_ROVER_V2_Drawing_v4.pdf` (Fusion 360, mm, 3 sheets, J. Morales 2026-10-01). Not stored in the repo yet.
- Status: Read by the app; items marked **(derived)** are computed from the drawing, items marked **(to confirm)** await Jan.

## Frame convention
- CAD origin = **rear axle center** (sheet 3). Proposed `base_link` = CAD origin; `base_footprint` = projection on the ground (z = −66.76 mm).
- Axes (REP-103): x forward (toward the depth camera), y left, z up.

## Dimensions
| Item | Value (mm) | Source |
|---|---|---|
| Wheel radius (axle → ground) | 66.76 | Dimensioned |
| Wheelbase (rear axle → front axle) | 202.33 | Dimensioned |
| Overall width over tires | 323.98 | Dimensioned |
| Wheel width | ≈ 65.6 | Derived from scale, confirmed by Jan |
| **Track width (wheel center to wheel center)** | **≈ 258.4** = 323.98 − 65.6 | Derived, confirmed by Jan |
| Chassis width / rear section / LiDAR mount | 166 / 165.8 / 115 | Dimensioned |
| Width over motor shafts | 244 | Dimensioned |
| Ground clearance | 43.55 | Dimensioned |
| Overall height | 179.57 | Dimensioned |
| Overall length (depth camera face → rear tire) | ≈ 330 = 263.21 + 66.76 | Derived |
| Lower deck → upper deck | 52 | Dimensioned (Jan: lower = Pi, motors, depth camera; upper = battery, live camera, LiDAR) |

## Sensor poses relative to the origin
| Sensor | x | y | z | Orientation | Notes |
|---|---|---|---|---|---|
| D435 front glass, **2nd lens from the viewer's left (IR projector)** | +263.21 | −11.19 (confirmed: rover's right) | +3.61 (confirmed: above axle) | Level, facing forward | Not the ROS reference. realsense-ros `camera_link` = depth origin = **left imager**, named from the camera's own view → **3rd lens from the viewer's left** in a front view. Needed: y, z of that lens (Jan to measure in Fusion); Code to verify lens identity by covering a lens and watching which IR stream goes dark |
| Mid-360 **center of the bottom face of the base** (confirmed) | +4.52 | 0 | +60.53 | Pitched 45°, sensor z-axis pointing **up and backward** → URDF rpy = (0, −π/4, 0) | Must be converted to the Livox point-cloud origin as defined in the Mid-360 manual (the IMU sits at z = −44.12 mm in the LiDAR frame, so the frame origin is well above the base) |

Design intent (Jan): the LiDAR maps the section already travelled; the depth camera previews what is ahead.

## Drivetrain
| Item | Value |
|---|---|
| Configuration | 4-wheel skid steer |
| Rear motors | 150:1 37D×73L gearmotor, 12 V, 64 CPR encoder → 64 × 150 = **9,600 counts/wheel rev** → **0.0437 mm/count** (circumference 419.5 mm) |
| Front motors | 10 RPM, 12 V, no encoders (chosen for torque) |
| Speed at 10 RPM | 70 mm/s (4.2 m/min; 100 m ≈ 24 min) |

Speed mismatch: the rear motors are faster (no-load speed to be taken from the datasheet). Deferred by Jan (to be solved with the electronics). Proposed mitigation: closed-loop speed control on the rear wheels, with the rear setpoint matched to the measured loaded speed of the front motors, so the front wheels neither drag nor are dragged. A second pair of 150:1 motors (without encoders) is a fallback; electronics to be discussed later.

## Consequences for localization
- Wheel odometry: distance on straight runs only; heading from the Mid-360 IMU (skid steer slips in turns). Treat wheel odometry as a low-weight input.
- The LiDAR is the primary measurement source (Jan).
- The rover body (battery, live-feed camera tower) is in the LiDAR's field of view: apply a crop box around the body before SLAM.
