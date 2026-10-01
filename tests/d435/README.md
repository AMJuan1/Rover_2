# Intel RealSense D435 — standalone test (ADR-005)

> **Unit on hand is a D435 (USB PID 0x0B07), not a D435i (PID 0x0B3A): no IMU.** Detected 2026-10-01.

No ROS in this phase: test with the librealsense2 SDK tools only (`realsense-viewer`, `rs-enumerate-devices`, `rs-fw-update`).

## Key specs (Intel D400 datasheet)

| Item | Value |
|---|---|
| Interface / power | USB-C 3.1 Gen 1 (5 Gbit/s), bus powered. USB 2 works but limits resolution/fps |
| Depth | Active IR stereo, global shutter, baseline 50 mm; up to 1280×720 @ 30 fps, 848×480 @ 90 fps |
| Depth FOV | 87° × 58° |
| Min depth (min-Z) | ~0.28 m at 1280×720; lower at 848×480 / 640×480 |
| Ideal range | ~0.3–3 m (usable to ~10 m, error grows with distance²) |
| RGB | 1920×1080 @ 30 fps, rolling shutter, FOV 69° × 42° |
| IMU | **None on D435.** (D435i only: Bosch BMI055 accel 63/250 Hz, gyro 200/400 Hz) |
| Firmware | SDK 2.58.x recommends D400 FW ≥ 5.17.3.10. Unit has 5.13.0.55 |

## Software (Linux, no ROS)

| Package | Source | Size | Purpose |
|---|---|---|---|
| `librealsense2-utils` v2.58.4 (+ `librealsense2`, `-gl`, `-udev-rules` deps) | RealSense apt repo `librealsense.realsenseai.com/Debian/apt-repo` (jammy) | ~20 MB | `realsense-viewer`, `rs-enumerate-devices`, `rs-fw-update`, udev rules |
| `librealsense2-dkms` | same repo | 0.6 MB | Kernel patches. **Supports kernels 5.15/5.19/6.5 only; dev laptop runs 6.8 → skip.** Stock 6.8 `uvcvideo` handles depth/RGB; per-frame metadata (HW timestamps) may be partial |

## Dev-machine notes
- Kernel 6.8.0-85-generic, Secure Boot disabled.
- Plug the camera **directly into a laptop USB 3 port**, not the Anker hub that carries the LiDAR's Ethernet adapter.

## Results
See `docs/research/hardware-tests.md` (per-device results section).
