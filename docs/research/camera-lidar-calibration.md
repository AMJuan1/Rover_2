# Camera–LiDAR extrinsic calibration (Mid-360 + D435)
- Date: 2026-10-01
- Status: Research note (app), answers hand-off 2026-10-01 "Combined sensor view" request #2
- Goal: find the rigid transform between the D435 color camera and the Mid-360 (`T_lidar_camera`), to replace the placeholder static TF in `tests/combined/sensors.launch.py` and later the URDF.

## Recommended procedure
| Step | Method | Output |
|---|---|---|
| 0 | **CAD prior** from Jan's prototype 3D model: positions/orientations of the Mid-360 origin and the D435 mounting reference | Initial guess (expected error: a few mm to cm, a few degrees) |
| 1 | **Targetless calibration with `direct_visual_lidar_calibration`** (koide3; ROS 1/ROS 2; MIT license; supports non-repetitive Livox scans and pinhole cameras) | `T_lidar_camera` (camera optical frame → LiDAR frame) in `calib.json` |
| 2 | **Independent check with D435 depth**: ICP (Open3D, point-to-plane) between a static D435 depth cloud and an accumulated Mid-360 cloud, initialized from step 1 | Agreement check (D435 depth→color extrinsic is factory-calibrated) |
| 3 | **Visual check**: project LiDAR points onto the RGB image (edges, corners must line up) | Accept / repeat |

### Step 1 details (direct_visual_lidar_calibration)
1. Mount both sensors **rigidly** in their final relative position (any change later requires recalibration).
2. Record 3–5 short **static** bags in a structured, well-lit room (walls, furniture, edges; **not inside a pipe**): `/livox/lidar` (PointCloud2), `/camera/camera/color/image_raw`, `/camera/camera/color/camera_info`. Hold each pose ~10–20 s so the Mid-360 non-repetitive pattern fills in a dense cloud. Use fixed exposure.
3. Preprocess: `ros2 run direct_visual_lidar_calibration preprocess <bags_dir> <out_dir> -av`
4. Initial guess: **manual** (`initial_guess_manual`, ≥ 3 point pairs) or the CAD prior. The automatic SuperGlue option carries a **non-commercial-use restriction** — avoid it for this product.
5. Fine registration: `ros2 run direct_visual_lidar_calibration calibrate <out_dir>`
6. Result `T_lidar_camera: [x, y, z, qx, qy, qz, qw]` refers to the **color optical frame**. Convert to `camera_link` using the D435 internal TF published by `realsense2_camera` (`camera_link → camera_color_optical_frame`).
- Camera intrinsics: use the D435 factory values from `camera_info` (no separate intrinsic calibration needed unless the reprojection check fails).
- Docker images are provided by the project (useful to avoid dependency conflicts with the rover workspace).

## Alternative (target-based, higher accuracy, production use)
**FAST-Calib** (HKU MARS, 2025): custom 3D board with four circular holes + four ArUco markers; reported point-to-point error < 6.5 mm, < 0.7 s per run; explicitly supports Livox Mid-360. Requires building the board; ROS version to be verified. Consider it if step 1 accuracy is insufficient or for repeatable calibration of several rovers.

## Acceptance criteria (proposed)
| Check | Target |
|---|---|
| Difference vs CAD prior | < 2 cm, < 2° (larger = suspect CAD or calibration) |
| ICP vs step 1 translation | < 1 cm |
| Projection of LiDAR edges on image | visually aligned at 1–3 m |

## Notes
- Time sync is not critical for static calibration; it matters later for colorizing while moving (Mid-360 supports PTP; D435 uses its own clock → software sync / hardware timestamps to be studied).
- Store the result in `config/` as YAML and publish it via the URDF (`livox_frame → camera_link` joint), replacing the placeholder in `tests/combined/`.

## Sources
- https://github.com/koide3/direct_visual_lidar_calibration
- https://koide3.github.io/direct_visual_lidar_calibration/example/
- https://arxiv.org/html/2507.17210v1 (FAST-Calib)
