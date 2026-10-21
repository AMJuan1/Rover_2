# Control board V2.1 — bench test procedures and scripts
- Date: 2026-10-20
- Status: Procedures written by the app and run by Jan on the dev laptop. Results are in `hardware-tests.md`.
- Scripts were run with MicroPython 1.29.0 on the Pico 2 via `mpremote` from `~/pico_tests/` on the dev laptop. They are reproduced here so they survive outside that folder. @code may move them to `tests/control_board/`.
- Safety: any script that turns a motor is run only after Jan confirms the motor is clamped or the wheel is off the ground (CLAUDE.md workflow rule).

## Status
| Module | Procedure | Result |
|---|---|---|
| Buck "XL4016" (marketplace) | No-load CV/CC procedure | FAIL: wrong item (UC3843 boost). Replacement pending |
| Pico 2 | `selftest.py` + ADC jumper test | PASS |
| XY-MOS dual D4184 | `mos_test.py` (GP21 trigger) | PASS |
| DRV8871 module 1 + one motor | `drv_motor.py`, `drv_motor2.py` (GP16/17) | PASS (slow decay only) |
| Encoder (same motor) | `enc_test.py` (GP18/19 temporary) | **Next — handed to Claude Code** |
| DRV8871 modules 2–4, other 3 motors/encoders | Same scripts | Pending |
| Servos, WS2812B, VBAT divider, e-stop, buck B | — | Pending |

## Common wiring used so far
| Signal | Pico 2 pin (physical) |
|---|---|
| DRV8871 IN1 / IN2 | GP16 (21) / GP17 (22) — RR motor pins in the final pin map |
| DRV8871 header GND | GND (23) |
| XY-MOS TRIG / GND | GP21 (27) / GND (28) |
| Encoder A / B (temporary) | GP18 (24) / GP19 (25) through 1 kΩ series resistors (final: GP8/GP9 for RR) |
| Encoder Vcc / GND | VBUS (40, 5 V from USB) / GND (38) |
| Motor supply | Bench supply 12 V, 1.5 A limit → DRV8871 VM / GND terminals. Header VM is never connected to the Pico |

## Encoder test (next)
Pololu 37D encoder wire colours: red/black = motor, blue = encoder Vcc (3.5–20 V), green = encoder GND, yellow = A, white = B. 64 counts per motor revolution (both edges, both channels) × 150 = **9,600 counts per output revolution**.

```python
# ~/pico_tests/enc_test.py
from machine import Pin, PWM
import time
A, B = 18, 19            # temporary; final design uses GP8/GP9 for RR
IN1, IN2, F = 16, 17, 20000
CPR_OUT = 9600           # 64 counts/motor rev x 150

pa = Pin(A, Pin.IN); pb = Pin(B, Pin.IN)
count = 0
errors = 0
last = (pa.value() << 1) | pb.value()
T = (0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0)
def isr(p):
    global count, last, errors
    s = (pa.value() << 1) | pb.value()
    i = (last << 2) | s
    if i in (3, 6, 9, 12):
        errors += 1
    count += T[i]
    last = s
pa.irq(isr, Pin.IRQ_RISING | Pin.IRQ_FALLING, hard=True)
pb.irq(isr, Pin.IRQ_RISING | Pin.IRQ_FALLING, hard=True)

p1 = PWM(Pin(IN1), freq=F, duty_u16=0); p2 = PWM(Pin(IN2), freq=F, duty_u16=0)
def drive(d1, d2):
    p1.duty_u16(65535 * d1 // 100); p2.duty_u16(65535 * d2 // 100)

def run(label, d1, d2, s):
    global count
    drive(d1, d2); time.sleep(1)          # let speed settle
    c0 = count; t0 = time.ticks_ms(); time.sleep(s)
    dc = count - c0; dt = time.ticks_diff(time.ticks_ms(), t0) / 1000
    rpm = dc / CPR_OUT / dt * 60
    print("%-14s counts=%7d  output RPM=%6.1f" % (label, dc, rpm))

try:
    print("Phase 1: motor OFF. Turn the output shaft slowly by hand, ONE full turn forward, within 15 s")
    count = 0; time.sleep(15)
    print("Hand turn: counts=%d (expect ~ +/-9600), errors=%d" % (count, errors))
    print("Phase 2: motor runs (clamped)")
    run("FWD 30 %", 100, 70, 5)
    run("FWD 60 %", 100, 40, 5)
    drive(100, 100); time.sleep(1)
    run("REV 30 %", 70, 100, 5)
    drive(100, 100); time.sleep(1)
    print("Encoder errors (missed edges): %d" % errors)
finally:
    drive(0, 0); p1.deinit(); p2.deinit()
    Pin(IN1, Pin.OUT, value=0); Pin(IN2, Pin.OUT, value=0); print("Done: COAST")
```
Run: `mpremote connect /dev/ttyACM0 run ~/pico_tests/enc_test.py`

| Check | Pass |
|---|---|
| Hand turn, 1 output revolution (or ½ turn ≈ 4,800) | ≈ ±9,600 counts (±5 %) |
| FWD 30 % / 60 % (slow decay) | Positive counts; RPM rises with duty |
| REV 30 % | Negative counts; RPM similar to FWD 30 % |
| Encoder errors | 0 or a few. Many errors at 60 % → MicroPython IRQ too slow (≈ 6–7 kHz edges); acceptable here, since the final firmware uses PIO |

If hand-turn and forward-drive signs disagree, swap yellow/white; only consistency matters.

## Motor drive rules found on the bench (DRV8871 + Pololu 150:1, 20 kHz)
- Fast decay (one input PWM, other low) gives no motion at 20/50 %. Use **slow decay only**: forward IN1 = 1, IN2 = PWM at (1 − d); reverse mirrored.
- Start threshold, no load: 15 % trembles; steady from ≈ 20 %.
- Brake = both inputs high; coast = both low.
- R_ILIM fitted = 30 kΩ (code 303) → I_trip ≈ 2.1 A; kept.

## Earlier scripts (for repeating on modules 2–4)
```python
# ~/pico_tests/drv_motor2.py — slow-decay sweep and reverse
from machine import Pin, PWM
import time
IN1, IN2, F = 16, 17, 20000
p1 = PWM(Pin(IN1), freq=F, duty_u16=0); p2 = PWM(Pin(IN2), freq=F, duty_u16=0)
def set_duty(d1, d2):
    p1.duty_u16(65535 * d1 // 100); p2.duty_u16(65535 * d2 // 100)
def fwd(d): set_duty(100, 100 - d)
def rev(d): set_duty(100 - d, 100)
try:
    for d in (10, 15, 20, 25, 30, 40):
        fwd(d); print("FWD slow-decay %d %%" % d); time.sleep(4)
    set_duty(100, 100); print("BRAKE"); time.sleep(2)
    for d in (30, 50, 100):
        rev(d); print("REV slow-decay %d %%" % d); time.sleep(4)
    set_duty(100, 100); print("BRAKE"); time.sleep(2)
finally:
    p1.duty_u16(0); p2.duty_u16(0); p1.deinit(); p2.deinit()
    Pin(IN1, Pin.OUT, value=0); Pin(IN2, Pin.OUT, value=0); print("Done: COAST")
```
`selftest.py` (Pico GPIO/ADC/PWM self-test) and `mos_test.py` (XY-MOS on GP21) are in `~/pico_tests/` on the dev laptop.
