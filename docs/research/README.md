# Research notes

One file per topic. Each file ends with a **Conclusion** section; if it leads to a design choice, add an ADR in `../decisions.md`.

| File | Topic | Status |
|---|---|---|
| `visualization.md` | RViz2 alternatives | TODO |
| `slam.md` | 2D/3D SLAM options (slam_toolbox, Cartographer, RTAB-Map) | TODO |
| `localization.md` | EKF sensor fusion (robot_localization) | TODO |
| `streaming.md` | Live camera feed to remote clients | TODO |
| `3d-reconstruction.md` | Point cloud → 3D model pipeline | TODO |
| `motor-control.md` | ros2_control, diff_drive_controller, PID tuning | TODO |

## Template

```
# <Topic>
- Date: YYYY-MM-DD
## Question
## Options found
| Option | Pros | Cons | ROS 2 support |
## Sources
## Conclusion
```
