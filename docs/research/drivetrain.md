# Drivetrain V2: motors, encoders, sizing
- Date: 2026-10-02
- Status: App analysis from the Pololu 37D datasheet (rev 1.2) supplied by Jan. Rover mass ≈ 1.9 kg (Jan, 2026-10-02).

## Motor (ADR-010): Pololu 150:1 Metal Gearmotor 37D×73L, 12 V, 64 CPR encoder (helical pinion)
| Parameter | Value (12 V) | Source |
|---|---|---|
| Gear ratio | 150:1 | Datasheet |
| No-load speed / current | 67 RPM / 0.2 A | Datasheet |
| Max efficiency point | 58 RPM, 65 kg·mm, 0.72 A, 3.8 W out | Datasheet |
| Stall (extrapolated) | 490 kg·mm, 5.5 A | Datasheet (units stall earlier as they heat) |
| Recommended load limits | ≤ 100 kg·mm continuous, ≤ 250 kg·mm instantaneous; ≤ 25 % of stall current (≈ 1.4 A) for longevity | Datasheet |
| Encoder | 2 Hall sensors, 64 CPR at the motor shaft (both edges, both channels) → **9,600 counts per wheel revolution**; Vcc 3.5–20 V, ≤ 10 mA; A/B outputs 0–Vcc | Datasheet |
| Leads | Red/black motor, green encoder GND, blue encoder Vcc, yellow A, white B | Datasheet |

## Derived values for the rover (wheel radius 66.76 mm, circumference 419.5 mm)
| Quantity | Value |
|---|---|
| Top speed (no load, 12 V) | 67 RPM → **0.47 m/s** (≈ 0.43 m/s at 11.1 V nominal) |
| Speed at max efficiency | 58 RPM → 0.41 m/s |
| Encoder rate at 67 RPM | ≈ 10,700 counts/s per motor → ≈ 43,000 counts/s for 4 motors |
| Odometry resolution | 0.044 mm per count |
| Continuous traction (4 × 100 kg·mm = 0.98 N·m each) | 14.7 N per wheel → **≈ 59 N total** |
| Instantaneous traction (4 × 250 kg·mm) | ≈ 147 N total |
| Rover weight (Jan: ≈ 1.9 kg with motors, Pi, LiDAR, cameras; wheels light) | ≈ 19–20 N → continuous traction ≈ **3 × weight**: ample for joint lips and pipe slopes |
| 100 m run time | ≈ 4 min one way at 0.4 m/s (vs ≈ 24 min at 70 mm/s with the 10 RPM motors) |

## Electrical sizing for the V2 board
| Item | Requirement |
|---|---|
| Driver channels | 4 independent, each ≥ 6 A peak (stall 5.5 A), ≥ 2 A continuous; current limiting or sensing preferred |
| Main fuse | ≈ 15 A (4 × ~1.5 A typical + electronics), slow-blow; confirm after measuring |
| Motor power while driving | ≈ 4 × 0.7 A × 12 V ≈ 35 W at the max-efficiency point; less on flat runs |
| Encoder supply | 5 V (3.3 V is below the 3.5 V minimum) → A/B are 5 V signals → **level shifting to 3.3 V required for the Pico 2** (e.g. 74LVC14 Schmitt buffer at 3.3 V with 5 V-tolerant inputs, also cleans edges) |
| PID | Closed loop on all 4 wheels; `diff_drive_controller` with two wheels per side |

## Battery runtime update
Shorter run times at 0.4 m/s cut the energy per mission substantially: a 100 m out-and-back is ≈ 8–10 min of driving instead of ≈ 48 min, so one 3S 6000 mAh pack becomes comfortable (supersedes the marginal estimate in `electronics.md`, to confirm by measurement).
