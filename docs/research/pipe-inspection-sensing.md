# Pipe-inspection sensing analysis
- Date: 2026-09-29
- Status: Initial analysis (app); to be validated by hardware tests (`hardware-tests.md`)

## Operating envelope (stated by Jan)
| Parameter | Value |
|---|---|
| Pipe internal diameter | 22–35 in (0.56–0.89 m); radius 0.28–0.44 m |
| Condition | Dry |
| Material | Concrete |
| Run length | ~100 m |
| Link | Tethered (no usable wireless under streets) |
| Lighting | On-board LEDs (already in v1) |

## Sensor fit
| Sensor | Assessment | To verify in tests |
|---|---|---|
| Livox Mid-360 | Blind zone 0.1 m is below the smallest wall distance (~0.28 m). Vertical FOV −7° to 52°: crown and invert near the rover are not seen instantly, but are covered from a short distance ahead as the rover advances. Concrete gives good returns. | Point density on walls/crown at 0.28–0.44 m; mounting height/tilt for full ring coverage |
| RealSense D435i | Minimum depth ~0.2–0.3 m (resolution dependent): usable only at the upper part of the range when looking at walls; forward depth along the pipe is fine. Active IR works regardless of light. RGB 1080p rolling shutter. | Depth fill rate on walls at 848×480 vs 1280×720; RGB texture quality with LED lighting while moving |
| Gimbal camera (not bought) | Size is not a constraint (SIYI A8 mini is 55×55×70 mm). Useful for operator inspection (joints, cracks, lateral connections). | Pitch range must reach the crown (+90°); check humidity/dust sealing |

## Key risks
1. **SLAM degeneracy along the pipe axis.** A straight, uniform concrete pipe gives LiDAR almost no constraint along its length; LIO can drift or slide. Mitigation: fuse wheel odometry + IMU, and add a **tether length counter** (encoder on the cable reel), the standard chainage reference in pipe inspection.
2. **Tether at 100 m.** Standard copper Ethernet is limited to 100 m per segment; a 100 m run plus slack exceeds it. Options: fiber-optic tether with media converters, long-range Ethernet extenders (VDSL/2-wire), or on-board recording with a low-bandwidth link. Decide before buying cable.
3. **Texture quality.** A forward-looking camera sees walls at grazing angles far ahead; texture resolution on walls may be poor. Mitigation candidates: wide-angle/fisheye fixed camera, gimbal locked in a known pose during mapping runs, or side-facing cameras.
4. **Bandwidth.** Raw LiDAR + depth + 4K video should be recorded on board; only compressed video and status go over the tether.

## Candidate pipelines (to research)
| Goal | Candidates |
|---|---|
| Colored point cloud / textured model from LiDAR + camera | FAST-LIVO2, R3LIVE (Livox-oriented LiDAR-inertial-visual) |
| RGB-D mapping | RTAB-Map with D435i |
| Mesh + texture post-processing | OpenMVS or similar, offline |

## Open questions
- On-board compute (current v1 board?) and power budget over tether vs battery.
- Required outputs for the client: video report only, or measured 3D model (accuracy target in mm?).
