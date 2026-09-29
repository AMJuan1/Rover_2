# Pipe-inspection sensing analysis
- Date: 2026-09-29
- Status: Initial analysis (app); to be validated by hardware tests (`hardware-tests.md`)

## Deliverables (stated by Jan)
| Priority | Deliverable | When |
|---|---|---|
| 1 | Live inspection video, good quality, with pan/tilt control | Live |
| 1 | Distance advanced + simple live 2D/3D map (Foxglove-style SLAM view) | Live |
| 2 | **As-built blueprint**: pipe length, direction and slope, exportable to CAD/GIS (many areas of the city have no blueprints) | Post-processing |
| 3 | Textured 3D model of the pipe | Post-processing |

## Operating envelope (stated by Jan)
| Parameter | Value |
|---|---|
| Pipe internal diameter | 22–35 in (0.56–0.89 m); radius 0.28–0.44 m |
| Condition | Dry concrete; frequent small protrusions at joints/connections |
| Run length | Usually < 100 m; 100 m maximum |
| Link | Tethered Ethernet (no usable wireless under streets) |
| Lighting | On-board LEDs (already in v1) |
| On-board computer | Raspberry Pi 4 (kept for now) |
| v1 localization | Wheel odometry only |

## Sensor fit
| Sensor | Assessment | To verify in tests |
|---|---|---|
| Livox Mid-360 | Blind zone 0.1 m < smallest wall distance (~0.28 m). Vertical FOV −7° to 52°: crown/invert near the rover are covered a short distance ahead as it advances. Concrete returns well. | Point density on walls/crown; mounting height/tilt |
| RealSense D435i | Min depth ~0.2–0.3 m: marginal on walls in 22" pipes, fine in 35" and forward along the pipe. Active IR independent of light. RGB 1080p rolling shutter. | Depth fill rate at 848×480; RGB texture with LEDs while moving; CPU load on Pi 4 |
| Gimbal camera (not bought) | Size not a constraint. Operator inspection. Streams its own encoded video (no encoding load on the Pi). | Pitch range to crown (+90°); dust/humidity sealing |

## Localization
- Joint protrusions give LiDAR SLAM features along the pipe axis, which largely avoids the "sliding" problem of perfectly smooth pipes. Risk remains that joints are periodic and similar (possible misalignment by one joint spacing).
- Fusion is the robust answer: **LiDAR-inertial SLAM + wheel odometry + IMU**. Wheels slip on protrusions (LiDAR corrects that); LiDAR can misalign on repetitive joints (wheels correct that).
- Tether length counter: optional, cheap backup for chainage; not required.

## Blueprint requirements
- Trajectory of the rover = pipe centerline (length, direction, slope). Pipe diameter from circle fit on LiDAR slices.
- **Georeferencing needed**: SLAM is relative. To place the pipe on a city map: GNSS position of the entry manhole + known initial heading (e.g. rover aligned to a surveyed direction, or GNSS at two points at the surface). A magnetometer is not reliable inside concrete with rebar.
- Export: polyline of the centerline to DXF (CAD) and GeoJSON/KML (GIS), with length, slope and diameter per segment.

## Compute and data flow (Raspberry Pi 4)
| Task | Where | Notes |
|---|---|---|
| Sensor drivers (Mid-360, D435i), motor control | Pi 4 | Verify CPU with both drivers running |
| Recording raw data (rosbag) | Pi 4 → USB 3 SSD | SD card is too slow for LiDAR + depth |
| Gimbal video | Gimbal → switch → tether → operator laptop | Bypasses the Pi |
| Live SLAM + map view (Foxglove) | Operator laptop (Ryzen 9) | Mid-360 raw stream ~200k pts/s fits in the Ethernet tether; move SLAM on board only if a stronger computer is added |
| 3D model, blueprint | Offline | From recorded bags |

- The Pi 4 has one Ethernet port: an **on-board Ethernet switch** is needed (Pi, Mid-360, gimbal, tether uplink).
- Tether: copper Ethernet is fine for usual runs; for full 100 m + slack, add a long-range Ethernet extender only if needed.
- Upgrade path if the Pi 4 is saturated: Raspberry Pi 5 or NVIDIA Jetson Orin Nano.

## Candidate pipelines (to research)
| Goal | Candidates |
|---|---|
| Live LiDAR-inertial SLAM (laptop) | FAST-LIO2, or similar Livox-compatible LIO |
| Colored point cloud / textured model (offline) | FAST-LIVO2, R3LIVE, RTAB-Map (D435i) |
| Mesh + texture | OpenMVS or similar, offline |

## Commercial reference: FJD Trion P2 handheld SLAM scanner (~USD 9,999)
LiDAR specs are identical to the Mid-360 (905 nm, 360°×59°, 200k pts/s, 40 m @ 10% / 70 m @ 80%), so it is most likely built around the same sensor. What it adds on top of the LiDAR:

| Component | Role |
|---|---|
| IMU, tightly coupled | LiDAR-inertial SLAM (real-time trajectory) |
| Front camera, 2 MP global shutter, 70° | Visual SLAM (extra constraint on the trajectory) |
| Two side cameras (12–48 MP, sources differ) | Color for the point cloud |
| Optional Insta360 X3/X5 on top | Panoramic imagery for texture |
| Factory camera–LiDAR calibration + hardware time sync | Makes the colorizing accurate |
| On-board real-time SLAM + desktop post-processing software | Fast live preview; accurate colored cloud / model offline |
| Optional RTK GNSS | Georeferencing (not usable inside pipes) |

Implications for the rover: the Mid-360 + built-in IMU already cover the core. Missing pieces are a fixed, calibrated, time-synchronized color camera and the software pipeline (open-source equivalents: FAST-LIVO2, R3LIVE). **A 360° camera is a strong texture candidate in pipes**: it sees the whole pipe ring at once, avoiding the grazing-angle problem of a forward camera. Requires even LED lighting around the rover and a sync/alignment method with the LiDAR (to research).
