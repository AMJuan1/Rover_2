# Control board V2.1 — prototype from off-the-shelf modules
- Date: 2026-10-02
- Status: Design draft (app) for Jan's review. Diagram: Lucidchart "ROVER V2 - Control Board 2.1 (prototype modules)" (4 pages: power tree, signals, Pico 2 pin map, modules).
- Purpose: validate every function with separate, replaceable modules on a Raspberry Pi proto HAT + wiring, before designing the production PCB (V3). Based on v1 board concepts (Pi HAT, MCU over USB, buck for 5 V, motor driver, servos, LEDs) plus everything decided since (ADR-006, -009, -010, -011, `pcb-review.md`, `drivetrain.md`).

## Changes vs v1 board
| v1 (`pcb-review.md`) | V2.1 |
|---|---|
| Arduino Nano, 2 encoders | **Pico 2 (RP2350)**, 4 encoders in PIO (ADR-011) |
| One L298N, 2 motors in parallel per channel | **2× Cytron MDD10A** (dual 10 A) → 4 independent channels |
| 1 front + 1 rear motor type | 4× Pololu 150:1 encoder motors (ADR-010) |
| Single 5 V buck for everything | **Two bucks**: logic (Pi, USB, encoders) and actuators (servos, LEDs) |
| Servos on Pi GPIO17/18 (software PWM) | Servos on **Pico hardware PWM** |
| LED_CONTROL on Pi GPIO15 (can't drive WS2812B) | WS2812B from **Pico PIO** through **74AHCT125** (3.3→5 V) |
| No battery monitoring | VBAT divider → Pico ADC0 + standalone LiPo cell alarm |
| No fuse / switch / e-stop | Main switch, 15 A main fuse, fused distribution, **e-stop on motor branch** with state sensed by the Pico |
| Encoders read at 5 V by the Nano | Encoders at 5 V → **BSS138 level shifters** → 3.3 V Pico |
| Pi USB ports powering everything | **Powered USB 3 hub** for D435 + SSD |

## Power tree
| Branch | Fuse (blade) | Feeds | Notes |
|---|---|---|---|
| Battery → main switch (20 A) → main fuse 15 A → 6-way fuse box | — | VBAT 9.9–12.6 V | 3S 6000 mAh; LiPo cell checker/buzzer on the balance lead |
| F1 motors | 10 A | E-stop (latching mushroom) → 2× MDD10A → 4 motors | Stall 5.5 A each: a simultaneous stall blows F1 (intended) |
| F2 logic | 5 A | Buck A, XL4016 set to **5.1 V** | Pi 4 (via HAT pins 2/4 + 3 A polyfuse), powered USB 3 hub, encoders (4 × 10 mA). Peak ≈ 4–4.5 A → heatsink, measure |
| F3 actuators | 5 A | Buck B, XL4016 set to **5.0 V** | 2 servos, WS2812B (cap brightness ≈ 2 A in firmware), camera LED. Peak ≈ 4 A |
| F4 LiDAR | 3 A | Mid-360 direct (9–27 V) via its splitter cable | 6.5 W nominal, 18 W for ~8 s at start-up |
| F5 network | 2 A | Mini Ethernet switch (12 V model, or 5 V from buck A) | |
| — | — | VBAT divider 10 k / 3.3 k + 100 nF → Pico ADC0 | 12.6 V → 3.13 V (max ADC 3.3 V) |

- **No boost converter is needed**: no load requires more than VBAT.
- Common ground: star point at the fuse box negative bus; MDD10A logic GND tied to Pico GND.
- Pico 2 is powered from the Pi's USB (same cable as the serial link), as in v1.

## Signals and data
- Tether (Cat6) → 5-port switch → Pi 4 and Mid-360 (Ethernet; PTP time sync later).
- Pi 4 USB: powered USB 3 hub (D435, SSD) · Arducam (USB 2) · Pico 2 (USB serial).
- Pico 2: see pin map.

## Pico 2 pin map
| GPIO | Function | Connects to |
|---|---|---|
| GP0 / GP1 | I2C0 SDA / SCL (spare) | Future INA226 current/voltage monitor, sensors |
| GP2 / GP3 | Encoder FL A / B (PIO) | Level shifter #1 |
| GP4 / GP5 | Encoder RL A / B (PIO) | Level shifter #1 |
| GP6 / GP7 | Encoder FR A / B (PIO) | Level shifter #2 |
| GP8 / GP9 | Encoder RR A / B (PIO) | Level shifter #2 |
| GP10 / GP11 | FL PWM / DIR | MDD10A #1 ch1 |
| GP12 / GP13 | RL PWM / DIR | MDD10A #1 ch2 |
| GP14 / GP15 | FR PWM / DIR | MDD10A #2 ch1 |
| GP16 / GP17 | RR PWM / DIR | MDD10A #2 ch2 |
| GP18 / GP19 | Servo pan / tilt (hardware PWM, 50 Hz) | Servos (signal 3.3 V) |
| GP20 | WS2812B data (PIO) | 74AHCT125 → strips (5 V) |
| GP21 | Camera LED on/off | D4184 MOSFET module gate |
| GP22 | E-stop state input | Divider 10 k / 3.3 k on motor branch after the e-stop |
| GP26 (ADC0) | Battery voltage | VBAT divider |
| GP27, GP28 (ADC1–2) | Spare | Future motor current sensing |
| GP25 | On-board LED | Heartbeat |
| USB | Serial to Pi + 5 V power | Raspberry Pi 4 |

Encoder pairs are on consecutive pins (required by the PIO quadrature program). PWM pins use separate slices (GP10/12/14/16 → slices 5/6/7/0; GP18/19 → slice 1).

## Modules (BOM)
| Block | Part | Qty | Notes |
|---|---|---|---|
| Controller | Raspberry Pi Pico 2 (RP2350) | 1 | ADR-011 |
| Motor drivers | Cytron MDD10A (dual 10 A, PWM + DIR, 3.3/5 V logic) | 2 | Sign-magnitude PWM up to 20 kHz |
| Motors | Pololu 150:1 37D×73L 12 V, 64 CPR encoder | 4 | ADR-010 |
| Logic buck | XL4016 module (as v1), set 5.1 V | 1 | Heatsink |
| Actuator buck | XL4016 module, set 5.0 V | 1 | |
| Level shift (in) | BSS138 4-channel module | 2 | 8 encoder signals |
| Level shift (out) | 74AHCT125 (DIP-14) | 1 | WS2812B data |
| LED switch | D4184 MOSFET module | 1 | Logic-level gate |
| Protection | Rocker switch 20 A, inline 15 A blade fuse, latching e-stop | 1 set | |
| Distribution | 6-way blade fuse box | 1 | 10 / 5 / 5 / 3 / 2 A |
| Battery monitor | 10 k + 3.3 k + 100 nF; LiPo cell checker with buzzer | 1 | |
| USB | Powered USB 3 hub | 1 | Off the Pi's 1.2 A USB budget |
| Network | 5-port mini Ethernet switch | 1 | |
| Carrier | Raspberry Pi proto HAT + stacking header, polyfuse 3 A | 1 | Mount Pico 2, shifters, 74AHCT125, dividers |
| Connectors | XT60 (EC5 adapter), JST/Dupont for encoders, screw terminals | — | Strain relief on all motor/encoder leads |

## Firmware/software implications
- Pico 2 firmware (Arduino-Pico core or Pico SDK): port of `ros_arduino_bridge` concepts — ASCII protocol extended to 4 motors (`e` → 4 counts; `m a b c d`; `o a b c d`; `u Kp:Kd:Ki:Ko`), PID per wheel, 2 s auto-stop, plus: battery voltage, e-stop state (zero PWM while open), servo angles, LED commands.
- ROS 2: fork `diffdrive_arduino` → 4 joints; `diff_drive_controller` with two wheels per side; `twist_mux` + gamepad dead-man as in v1.

## Bench test order (one module at a time)
1. Power tree without loads: set both bucks with a multimeter (5.1 V / 5.0 V); check fuses and e-stop.
2. Pi 4 + HAT + Pico 2 over USB: serial echo, heartbeat LED.
3. One MDD10A channel + one motor, open-loop PWM (wheel lifted).
4. One encoder through the level shifter: PIO counts, 9,600 counts per wheel revolution.
5. Closed-loop PID on one wheel; then all four.
6. Servos, WS2812B (brightness cap), camera LED.
7. Battery ADC calibration against a multimeter; e-stop input.
8. Full load: motors + Mid-360 + D435 + recording (hardware test 9).
