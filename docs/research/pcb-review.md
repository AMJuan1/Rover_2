# Review of Jan's control PCB (v1 board, `PCB.pdf`, KiCad)
- Date: 2026-10-01
- Status: App review of the schematic (3 sheets). Not stored in the repo. Items marked (to confirm) await Jan.

## What the board contains
| Block | Implementation |
|---|---|
| Power input | J3 battery in (VCC = 3S LiPo) |
| 5 V supply | XL4016E1 buck, 47 µH (SMMS1770-470M), MBR1645 Schottky, 470 µF in / 1000 µF out. Feedback 10 k / 3.3 k → Vout = 1.25 × (1 + 10/3.3) ≈ **5.04 V** |
| Motor driver | One **L298N** (dual H-bridge). Channel A (OUT1/2) = right side, channel B (OUT3/4) = left side. EnA/EnB tied to +5 V via J6/J7; speed by PWM on IN1–IN4. Flyback diodes: 8× 1N4007, 220 µF on VCC |
| Motor connectors | J1/J2 (6-pin): right/left **main** motors with encoder (OUT±, GND, +5 V, A, B). J9/J10 (2-pin): right/left **second** motors, **in parallel** with the main motor of the same side |
| Microcontroller | Arduino Nano: IN1 = D6, IN2 = D10 (left); IN3 = D9, IN4 = D5 (right) — all PWM pins. Encoders: L-a = D2, L-b = D3 (external interrupts); R-a = A4, R-b = A5 (pin-change interrupts only). JP1 (open) links +5 V to the Nano **VIN**; JP2 (open) links Nano GND |
| Raspberry Pi header | Pi powered from +5 V on pin 2. LED_CONTROL = GPIO15 (pin 10); SERVO1 = GPIO17 (pin 11); SERVO2 = GPIO18 (pin 12, PWM0) |
| Peripherals | J11 LED (+5 V, GND, LED_CONTROL); J4 two servos (+5 V, GND, control); J8 "battery level" (VCC, GND only) |

## Findings
| # | Finding | Impact | Suggestion |
|---|---|---|---|
| 1 | **Front and rear motors of each side share one L298N channel** (J1 ∥ J9, J2 ∥ J10) | They always get the same voltage, so the 10 RPM front and the faster 150:1 rear cannot be speed-matched. The front motors (high reduction, not back-drivable) act as a brake: the rear wheels slip, the **rear encoders over-count**, and current/heat rise | Four independent channels (two dual drivers), so the rear can be throttled to the front speed |
| 2 | **L298N** is bipolar: ~2–4 V drop and ~2 A per channel continuous, here with **two motors per channel** | Motors see ~8–9 V from an 11.1 V pack; overheating/current limiting under load. Possibly part of v1's "lack of torque" | MOSFET drivers (e.g. 2× dual 10 A class drivers); keep the Nano |
| 3 | JP1 feeds +5 V into the Nano **VIN** (regulator input, needs ~7 V+) | If closed, the Nano runs at ~4 V | Feed the +5 V pin instead, or power the Nano from the Pi's USB (also the serial link) |
| 4 | Pi ↔ Nano link not on the schematic | — | (to confirm) USB cable Pi → Nano (serial + power)? |
| 5 | LED_CONTROL on **GPIO15 (UART RX)** | WS2812B libraries on the Pi only drive GPIO 10 (SPI), 12/18 (PWM), 13/19 (PWM1) or 21 (PCM). 3.3 V data with 5 V LEDs also needs a level shifter | Move to GPIO10 (SPI) or GPIO21 + 74AHCT125, or let the Nano drive the LEDs |
| 6 | SERVO1 on GPIO17 (no hardware PWM) | Software PWM → servo jitter | Use `pigpio` (DMA-timed) or GPIO12/13; or drive servos from the Nano |
| 7 | Single 5 V rail for Pi + servos + LEDs + encoders + L298N logic | Servo/LED current spikes can brown out the Pi (under-voltage below ~4.63 V) | Separate buck for servos/LEDs; set the Pi rail to 5.1–5.2 V (R3 ≈ 3.2 k) |
| 8 | Pi powered through header pin 2 | Bypasses the USB-C input; no protection | Acceptable if the rail is clean; add a fuse/TVS on +5 V |
| 9 | J8 "battery level" has no divider / ADC input | No battery monitoring | Divider (e.g. 10 k / 3.3 k → 12.6 V ≈ 3.1 V) to a Nano analog pin (A0) |
| 10 | No fuse, switch or reverse-polarity protection on J3 | A 120C LiPo can deliver very high fault current | Inline fuse + main switch at the battery; e-stop |
| 11 | 1N4007 flyback diodes are slow-recovery | Minor losses with PWM | Fast/Schottky diodes (e.g. 1N5819/UF4007), or drivers with internal protection |
| 12 | Right encoder on A4/A5 | A4/A5 are the Nano's I²C pins → I²C unavailable | Acceptable; note for future sensors |

## Good points
- XL4016 buck is a solid choice for 5 V from 3S (high current capability with heatsinking).
- Encoders powered at 5 V and read by the 5 V Nano (no level shifting needed); left encoder on hardware interrupts.
- All motor inputs on PWM-capable pins; Nano as a real-time motor/encoder controller with the Pi on top is a sound split.
- Mid-360 and the Ethernet switch are not on this board: they need their own feeds (Mid-360 directly from VBAT 9–27 V).

## Software implications (for Claude Code, later)
- Nano firmware: PWM per channel, quadrature counting, serial protocol to the Pi.
- Pi: ROS 2 node or `ros2_control` hardware interface over USB serial; servo and LED control on the Pi (or on the Nano).
