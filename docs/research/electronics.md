# Electronics baseline (draft)
- Date: 2026-10-01
- Status: Draft by the app from Jan's inventory. Power figures are **estimates** to be replaced by measurements. Motor drivers: Jan's custom PCB, to be discussed next.

## Inventory (stated by Jan)
| Item | Model / spec | Notes |
|---|---|---|
| Battery | Zeee 3S LiPo 6000 mAh, 11.1 V nominal (12.6 V full), 66.6 Wh, 120C, EC5 (pack of 2) | Second pack available as spare / swap |
| Live-feed camera | Arducam USB 2.0, 1080p, 2 MP, automatic IR-cut, on-board IR LEDs (UVC) | Replaces the gimbal for now; mounted on pan/tilt **servos** |
| Camera light | One white LED on top of the live camera (moves with it), not dimmable | |
| Area lights | Treedix WS2812B 5 V addressable RGB LEDs (10×10 strips) around the rover | Brightness controllable in software |
| Motor drivers | Jan's custom PCB | Next topic |
| Tether | VOIETOLT Cat6 outdoor, 30 m, 24 AWG, **CCA** (copper-clad aluminium), waterproof jacket | Only 30 m; runs go up to 100 m |
| Operator side | Laptop only (USB-Ethernet adapter), charged from the car outlet | Rover runs on its own battery |

## Proposed power rails
| Rail | Source | Loads | Notes |
|---|---|---|---|
| VBAT 9.9–12.6 V | LiPo via main switch + fuse | Motors (via PCB), Mid-360 (9–27 V input) | Mid-360: 6.5 W nominal, up to 18 W for ~8 s at start-up |
| 5 V logic (≥ 5 A buck) | VBAT | Raspberry Pi 4 (5 V/3 A), D435 and Arducam via Pi USB, Ethernet switch (if 5 V) | Keep separate from servos and LEDs to avoid Pi brown-outs |
| 5–6 V servo (buck) | VBAT | Pan/tilt servos | Servo current spikes stay off the Pi rail |
| 5 V LED (buck, sized to software brightness limit) | VBAT | WS2812B strips, camera white LED | A WS2812B draws up to ~60 mA at full white: 100 LEDs could reach ~6 A. Cap brightness in software |

- WS2812B data line from the Pi (3.3 V) to 5 V LEDs: use a level shifter (e.g. 74AHCT125) — unless Jan's PCB already includes one.
- Battery monitoring: cell voltage / pack voltage to the Pi (ADC on the PCB?) with a low-voltage cutoff around 3.3–3.5 V per cell.

## Rough power budget (estimates, to measure)
| Load | Estimate |
|---|---|
| Mid-360 | 6.5 W |
| Raspberry Pi 4 (busy) | 5–7 W |
| D435 | 2–3.5 W |
| Arducam + IR LEDs | ~1 W |
| Servos (average) | 1–2 W |
| Lights (white LED + WS2812B, limited) | 5–10 W |
| 4 drive motors (moving, under load) | 25–45 W |
| **Total while driving** | **~45–75 W** |

- Usable energy per pack ≈ 80 % × 66.6 Wh ≈ 53 Wh → **~45–70 min** while driving.
- Mission time at 70 mm/s: 100 m in ≈ 24 min **one way**; the rover must also return (tethered), so ≈ 48 min of driving plus inspection stops. **One pack is marginal for a full 100 m run.** Options: swap packs, two packs in parallel (if the PCB allows), or measure real consumption first.

## Network and data
| Link | Plan |
|---|---|
| Pi 4 ↔ Mid-360 ↔ tether | Small on-board Ethernet switch (Pi has one port) |
| D435 | USB 3 to the Pi; raw depth + color recorded on an SSD |
| Arducam live feed | USB 2 to the Pi; MJPEG or Pi hardware H.264 → stream to the laptop (a few Mbit/s) |
| Tether budget | Mid-360 ≈ 23 Mbit/s + live video ≈ 2–10 Mbit/s + control: fits 100 Mbit/s |

Tether concerns:
1. **Length:** 30 m covers only short runs. Full runs need up to ~100 m + slack.
2. **CCA conductors:** higher resistance and more fragile than pure copper; acceptable at 30 m, risky near the 100 m Ethernet limit. Prefer pure-copper Cat6 (or a long-range Ethernet extender / fiber) for long runs.
3. Mechanical: strain relief at the rover, cable reel, protected connector at the rover end.

## Operator side
- Laptop power from the car: the dev laptop (Ryzen 9 + RTX 3060) uses a high-wattage adapter; a cigarette-lighter socket is typically fused at 10–15 A (~120–180 W). Use a pure-sine inverter or a 12 V laptop charger rated for the adapter, and check the socket fuse.

## Open questions for Jan
1. Custom PCB: which motor drivers, which voltages it generates, servo/LED outputs, ADC for battery voltage, connector to the Pi (GPIO header, USB, I2C)?
2. Servo model(s) for pan/tilt.
3. Main switch, fuse and emergency stop (remote stop from the laptop + physical switch).
4. Longer tether: pure copper, length target.
