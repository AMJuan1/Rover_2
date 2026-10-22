# Control board V2.1 — bench scripts (MicroPython, Pico 2)

Procedures and pass criteria: `docs/research/control-board-bench-procedures.md`. Results: `docs/research/hardware-tests.md`.
Any script that turns a motor runs only after Jan confirms the motor is clamped or the wheel is off the ground.

| Script | Motor turns | Purpose |
|---|---|---|
| `selftest.py` | No | Pico GPIO / ADC / PWM self-test |
| `drv_logic.py` | No | DRV8871 input logic check |
| `drv_motor.py`, `drv_motor2.py` | **Yes** | DRV8871 + motor: fast/slow-decay sweep, reverse, brake |
| `enc_common.py` | — | Shared quadrature decoder (IRQ) + slow-decay `Drive` class; must be copied to the Pico |
| `enc_hand.py` | No | Encoder phase 1: hand-turn one output revolution (expect ≈ ±9,600 counts) |
| `enc_motor.py` | **Yes** | Encoder phase 2: FWD 30 %, FWD 60 %, REV 30 % with counts, RPM and missed edges |

Bench wiring (temporary): DRV8871 IN1/IN2 = GP16/GP17, encoder A/B = GP18/GP19 via 1 kΩ, encoder Vcc = VBUS.

## Run (from this folder)
`sg dialout` is only needed in a shell started before the user joined `dialout`.
```bash
sg dialout -c "mpremote connect /dev/ttyACM0 cp enc_common.py : + run enc_hand.py"
```
```bash
sg dialout -c "mpremote connect /dev/ttyACM0 cp enc_common.py : + run enc_motor.py"
```
