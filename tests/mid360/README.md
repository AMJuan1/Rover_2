# Livox Mid-360 — standalone test (ADR-005)

Source: Livox Mid-360 User Manual v1.2 (2024-04), https://www.livoxtech.com/mid-360/downloads

## Key specs

| Item | Value |
|---|---|
| Supply | 9–27 V DC, **12 V recommended**; never exceed 27 V |
| Power | 6.5 W nominal; startup 18 W for ~8 s (<35 °C); self-heating up to 14 W for ≤10 min below 0 °C |
| Connector | M12 A-code 12-pin (male on sensor); 1-to-3 splitter cable: power (bare wires), Ethernet (RJ-45), function |
| Network | 100BASE-TX, UDP, static IP |
| Sensor IP | `192.168.1.1XX` (XX = last two digits of serial number), mask 255.255.255.0, gw 192.168.1.1 |
| Host IP | Sensor factory config sends to `192.168.1.5`; manual says `192.168.1.50`. Dev laptop has **both** on the adapter (NM profile `livox-mid360`) |
| Ports | LiDAR side 56100/56200/56300/56400/56500; host side 56101/56201/56301/56401/56501 (cmd/push/point/IMU/log) |
| FOV | 360° H, −7° to +52° V; blind zone 0.1 m; 40 m @ 10 % reflectivity |
| Point rate / frame | 200 k pts/s, 10 Hz default |
| IMU | Built-in 6-axis (3-axis accel + 3-axis gyro), 200 Hz; at x=11.0, y=23.29, z=−44.12 mm in lidar frame |
| Time sync | IEEE 1588-2008 (PTPv2 over UDP) or GPS (PPS pin 8 + GPRMC on pin 10, 9600 8N1) |
| Mounting | 4× M3 (5 mm deep) on the bottom; ≥10 mm clearance; metal plate ≥3 mm for heat |
| Protection | IP67 (sensor only); laser class 1 |

## Splitter-cable pinout

| Pin | Signal | Wire colour |
|---|---|---|
| 1, 9 | Power + (9–27 V) | Red |
| 2, 3 | Ground | Black |
| 4 / 5 | Ethernet TX+ / TX− | Orange-white / Orange |
| 6 / 7 | Ethernet RX+ / RX− | Green-white / Green |
| 8 | PPS in (3.3 V LVTTL) | Purple-white |
| 10 | GPS UART in (3.3 V LVTTL) | Gray-white |
| 11 / 12 | Reserved out (3.3 V) | Gray / Purple |

## Warnings (from manual)
- **Never plug the RJ-45 into a PoE port**: irreversible damage.
- Check polarity and voltage on the bench supply **before** connecting; set current limit ~2 A (startup peak 18 W ≈ 1.5 A @ 12 V).
- Don't point two LiDARs directly at each other.
- Don't wipe a dusty window dry; blow air first.

## Software

| Tool | Source | Needs ROS | Purpose |
|---|---|---|---|
| Livox Viewer 2 v2.3.0 (Ubuntu) | livoxtech.com downloads (~82 MB zip) | No | First power-on check, view cloud, set IP, read serial/firmware |
| Livox-SDK2 | github.com/Livox-SDK/Livox-SDK2 | No | C++ SDK; `livox_lidar_quick_start` sample; required by the ROS driver |
| livox_ros_driver2 | github.com/Livox-SDK/livox_ros_driver2 | Humble | Publishes `/livox/lidar` (PointCloud2 / CustomMsg) and `/livox/imu` |
| Firmware v13.18.0244 (2025-04-11) | livoxtech.com downloads (~5.6 MB) | No | Only if the unit is older; upgrade via Viewer 2 |

## Dev-machine notes (2026-09-30)
- The laptop has **no built-in Ethernet port** (only `wlp2s0` Wi-Fi). A USB-Ethernet adapter is required.
- Wi-Fi is on 192.168.0.0/24; no conflict with the LiDAR subnet 192.168.1.0/24.

## Results
See `docs/research/hardware-tests.md` (per-device results section).

## Dev-machine install (2026-09-30)
| Item | Location / status |
|---|---|
| Livox Viewer 2 v2.3.0 | `~/livox/LivoxViewer2/` (zip sha256 `e6b77ccd…5727af2`); launch `~/livox/LivoxViewer2/LivoxViewer2.sh`. Smoke-started OK without a sensor (UE4 app, RTX 3060, X11) |
| cmake | Pending (Jan runs `sudo apt install -y cmake`) |
| Livox-SDK2, livox_ros_driver2, ROS 2 Humble | Deferred by Jan |
