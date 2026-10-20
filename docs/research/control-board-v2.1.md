# Control board V2.1 — prototype from off-the-shelf modules
- Date: 2026-10-02
- Status: Design draft (app), revision 2 (2026-10-02: DRV8871 drivers, servo on the 5 V actuator rail, no encoder level shifters, inline fuses; ADR-013).
- Original status: Design draft (app) for Jan's review. Diagram: Lucidchart "ROVER V2 - Control Board 2.1 (prototype modules)" (4 pages: power tree, signals, Pico 2 pin map, modules).
- Purpose: validate every function with separate, replaceable modules on a Raspberry Pi proto HAT + wiring, before designing the production PCB (V3). Based on v1 board concepts (Pi HAT, MCU over USB, buck for 5 V, motor driver, servos, LEDs) plus everything decided since (ADR-006, -009, -010, -011, `pcb-review.md`, `drivetrain.md`).

## Changes vs v1 board
| v1 (`pcb-review.md`) | V2.1 |
|---|---|
| Arduino Nano, 2 encoders | **Pico 2 (RP2350)**, 4 encoders in PIO (ADR-011) |
| One L298N, 2 motors in parallel per channel | **4× DRV8871 modules** (one per motor, 3.6 A peak, adjustable current limit) → 4 independent channels |
| 1 front + 1 rear motor type | 4× Pololu 150:1 encoder motors (ADR-010) |
| Single 5 V buck for everything | **Two bucks**: logic (Pi, USB, encoders) and actuators (servos, LEDs) |
| Servos on Pi GPIO17/18 (software PWM) | Servos on **Pico hardware PWM** |
| LED_CONTROL on Pi GPIO15 (can't drive WS2812B) | WS2812B from **Pico PIO** (3.3 V data; 74AHCT125 buffer only if the strips flicker) |
| No battery monitoring | VBAT divider → Pico ADC0 + standalone LiPo cell alarm |
| No fuse / switch / e-stop | Main switch, 15 A main fuse, inline fuses on motor and LiDAR branches, **e-stop on motor branch** with state sensed by the Pico |
| Encoders read at 5 V by the Nano | Encoders at 5 V → **1 kΩ series resistor** per signal → Pico (RP2350 GPIOs are 5 V tolerant with IOVDD = 3.3 V; not the ADC pins GP26–29) |
| Pi USB ports powering everything | **Powered USB 3 hub** for D435 + SSD |

## Power tree
| Branch | Fuse | Feeds | Notes |
|---|---|---|---|
| Battery → main switch (20 A) → main fuse 15 A (inline blade) | 15 A | VBAT 9.9–12.6 V | 3S 6000 mAh; LiPo cell checker/buzzer on the balance lead |
| Motors | 10 A inline | E-stop (latching mushroom) → 4× DRV8871 → 4 motors | Driver current limit ≈ 2.9 A per motor (protects gearboxes, below 3.6 A driver peak) |
| Logic | (main) | Buck A, **5.1 V** (Jan's integrated buck, as v1) | Pi 4 (HAT pins 2/4 + 3 A polyfuse), powered USB 3 hub, encoders (4 × 10 mA), Ethernet switch if 5 V. Peak ≈ 4–4.5 A |
| Actuators | (main) | Buck B, XL4016 set to **5.0 V** | 2 servos (FT6335M stall 3.2–3.9 A), ~40 WS2812B (firmware cap 50 % ≈ 1.2 A). 1000 µF low-ESR at the servo connectors |
| Camera LED | small inline fuse (size from measured current) | **VBAT direct** → camera LED (12 V type) → XY-MOS (D4184) low-side switch | Brightness varies with battery (≈ 100 % at 12.6 V, ≈ 40 % at 9.9 V); constant-current driver is an open item for V3 |
| LiDAR | 3 A inline | Mid-360 direct (9–27 V) via its splitter cable | 6.5 W nominal, 18 W for ~8 s at start-up |
| — | — | VBAT divider 10 k / 3.3 k + 100 nF → Pico ADC0 | 12.6 V → 3.13 V (max ADC 3.3 V) |

- **Two bucks only** (A logic, B actuators). No 7 V servo rail: the FT6335M runs 4–8.4 V and worked at 5 V on v1.
- Servo stall current stays off the Pi rail (buck B). Firmware ramps servo moves to keep buck B peaks below its ≈ 5 A practical limit.
- Logic/actuator branch fuses (polyfuses) move onto the V3 PCB; V2.1 relies on the main fuse plus the bucks' own current limit.
- **No boost converter is needed**: no load requires more than VBAT.
- Common ground: star point at the main negative bus; DRV8871 GND tied to Pico GND.
- Pico 2 is powered from the Pi's USB (same cable as the serial link), as in v1.

## Signals and data
- Tether (Cat6) → 5-port switch (minimum 4: tether, Pi, Mid-360 + 1 spare) → Pi 4 and Mid-360 (Ethernet; PTP time sync later).
- Pi 4 USB: powered USB 3 hub (D435, SSD) · Arducam (USB 2) · Pico 2 (USB serial).
- Pico 2: see pin map.

## Pico 2 pin map
| GPIO | Function | Connects to |
|---|---|---|
| GP0 / GP1 | I2C0 SDA / SCL (spare) | Future INA226 current/voltage monitor, sensors |
| GP2 / GP3 | Encoder FL A / B (PIO) | 1 kΩ series |
| GP4 / GP5 | Encoder RL A / B (PIO) | 1 kΩ series |
| GP6 / GP7 | Encoder FR A / B (PIO) | 1 kΩ series |
| GP8 / GP9 | Encoder RR A / B (PIO) | 1 kΩ series |
| GP10 / GP11 | FL IN1 / IN2 (PWM) | DRV8871 #1 |
| GP12 / GP13 | RL IN1 / IN2 (PWM) | DRV8871 #2 |
| GP14 / GP15 | FR IN1 / IN2 (PWM) | DRV8871 #3 |
| GP16 / GP17 | RR IN1 / IN2 (PWM) | DRV8871 #4 |
| GP18 / GP19 | Servo pan / tilt (hardware PWM, 50 Hz, 500–2500 µs) | FT6335M pan + tilt servo (signal 3.3 V) |
| GP20 | WS2812B data (PIO) | 330 Ω series → strips (5 V); 74AHCT125 only if flicker |
| GP21 | Camera LED on/off | D4184 MOSFET module gate |
| GP22 | E-stop state input | Divider 10 k / 3.3 k on motor branch after the e-stop |
| GP26 (ADC0) | Battery voltage | VBAT divider |
| GP27, GP28 (ADC1–2) | Spare | Future motor current sensing |
| GP25 | On-board LED | Heartbeat |
| USB | Serial to Pi + 5 V power | Raspberry Pi 4 |

Encoder pairs are on consecutive pins (required by the PIO quadrature program). Each motor's IN1/IN2 pair is one PWM slice (GP10/11 → 5, GP12/13 → 6, GP14/15 → 7, GP16/17 → 0), both channels independent; servos GP18/19 → slice 1.

## Modules (BOM)
| Block | Part | Qty | Notes |
|---|---|---|---|
| Controller | Raspberry Pi Pico 2 (RP2350) | 1 | ADR-011 |
| Motor drivers | DRV8871 module, generic (6.5–45 V, 3.6 A peak, IN1/IN2, 3.3 V logic OK) | 4 (+1 spare) | Set R_ILIM ≈ 22 kΩ → I_trip = 64/22 ≈ 2.9 A (check the resistor fitted on the module) |
| Motors | Pololu 150:1 37D×73L 12 V, 64 CPR encoder | 4 | ADR-010 |
| Logic buck | Jan's integrated buck (as v1), set 5.1 V | 1 | Heatsink |
| Actuator buck | XL4016 module, set 5.0 V | 1 | |
| Encoder inputs | 1 kΩ resistors | 8 | Series, one per encoder signal |
| LED data | 330 Ω resistor; 74AHCT125 (DIP-14) optional | 1 | Buffer only if the strips flicker |
| Servos | Feetech FT6335M (4–8.4 V, 0–360°, stall 3.2–3.9 A) + tilt servo (Jan's, weaker) | 2 | Positional; 5 V from buck B |
| Servo rail capacitor | 1000 µF 10 V low-ESR | 1 | At the servo connectors |
| LED switch | XY-MOS dual D4184 module | 1 (+1 spare) | Low-side switch; TRIG from GP21; bench-tested 2026-10-20 |
| Protection | Rocker switch 20 A, latching e-stop | 1 set | |
| Fuses | Inline blade holders: 15 A main, 10 A motors, 3 A Mid-360 | 3 | Replaces the 6-way fuse box |
| Battery monitor | 10 k + 3.3 k + 100 nF; LiPo cell checker with buzzer | 1 | |
| USB | Powered USB 3 hub | 1 | Off the Pi's 1.2 A USB budget |
| Network | 5-port mini Ethernet switch (4 port minimum) | 1 | 3 ports in use: tether, Pi, Mid-360 |
| Storage | USB 3 SSD 256–512 GB | 1 | rosbag recording (Mid-360 + D435), on the powered hub |
| Carrier | Raspberry Pi proto HAT + stacking header, polyfuse 3 A | 1 | Mount Pico 2, series resistors, dividers |
| Connectors | XT60 (EC5 adapter), JST/Dupont for encoders, screw terminals | — | Strain relief on all motor/encoder leads |

## Firmware/software implications
- Pico 2 firmware (Arduino-Pico core or Pico SDK): port of `ros_arduino_bridge` concepts — ASCII protocol extended to 4 motors (`e` → 4 counts; `m a b c d`; `o a b c d`; `u Kp:Kd:Ki:Ko`), PID per wheel, 2 s auto-stop, plus: battery voltage, e-stop state (zero PWM while open), servo angles, LED commands.
- DRV8871 drive: 20 kHz PWM, slow decay (forward: IN1 = 1, IN2 = PWM with inverted duty; reverse mirrored) for linear low-speed control; both inputs low = coast, both high = brake.
- Pan/tilt: the gamepad stick sets a rate; the Pico integrates it into a target angle (clamped to limits) and ramps the servo. No angle feedback is required; the commanded angle is published for the inspection record, and a button recentres the camera.
- ROS 2: fork `diffdrive_arduino` → 4 joints; `diff_drive_controller` with two wheels per side; `twist_mux` + gamepad dead-man as in v1.

## Bench test order (one module at a time)
1. Power tree without loads: set both bucks with a multimeter (5.1 V / 5.0 V); check fuses and e-stop. Measure R_ILIM on each DRV8871 module.
2. Pi 4 + HAT + Pico 2 over USB: serial echo, heartbeat LED.
3. One DRV8871 + one motor, open-loop PWM (wheel lifted); verify current limit by briefly holding the wheel (≈ 2.9 A on a bench supply).
4. One encoder through 1 kΩ series resistors: PIO counts, 9,600 counts per wheel revolution.
5. Closed-loop PID on one wheel; then all four.
6. Servos, WS2812B (brightness cap), camera LED.
7. Battery ADC calibration against a multimeter; e-stop input.
8. Full load: motors + Mid-360 + D435 + recording (hardware test 9).
