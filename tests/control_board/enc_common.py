# Shared quadrature decoder and slow-decay drive for the encoder bench test (MicroPython, Pico 2).
# Pins are the temporary bench wiring; final RR pin map uses GP8/GP9 for the encoder.
from machine import Pin, PWM
import time

ENC_A, ENC_B = 18, 19       # yellow / white via 1 kOhm
IN1, IN2 = 16, 17           # DRV8871 #1 inputs
PWM_HZ = 20000
CPR_OUT = 9600              # 64 counts/motor rev x 150

# Transition table indexed by (last << 2) | now; +1 / -1 per valid edge, 0 otherwise.
_T = (0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0)
_INVALID = (3, 6, 9, 12)    # both channels changed at once = missed edge

_pa = Pin(ENC_A, Pin.IN)
_pb = Pin(ENC_B, Pin.IN)
count = 0
errors = 0
_last = (_pa.value() << 1) | _pb.value()


def _isr(_pin):
    global count, errors, _last
    s = (_pa.value() << 1) | _pb.value()
    i = (_last << 2) | s
    if i in _INVALID:
        errors += 1
    count += _T[i]
    _last = s


def start_decoder():
    _pa.irq(_isr, Pin.IRQ_RISING | Pin.IRQ_FALLING, hard=True)
    _pb.irq(_isr, Pin.IRQ_RISING | Pin.IRQ_FALLING, hard=True)


def coast_pins():
    """Hold both DRV8871 inputs low (coast)."""
    Pin(IN1, Pin.OUT, value=0)
    Pin(IN2, Pin.OUT, value=0)


class Drive:
    """Slow-decay drive: forward IN1=1, IN2=PWM(1-d); reverse mirrored; brake both high."""

    def __init__(self):
        self.p1 = PWM(Pin(IN1), freq=PWM_HZ, duty_u16=0)
        self.p2 = PWM(Pin(IN2), freq=PWM_HZ, duty_u16=0)

    def _set(self, d1, d2):
        self.p1.duty_u16(65535 * d1 // 100)
        self.p2.duty_u16(65535 * d2 // 100)

    def fwd(self, d):
        self._set(100, 100 - d)

    def rev(self, d):
        self._set(100 - d, 100)

    def brake(self):
        self._set(100, 100)

    def stop(self):
        self._set(0, 0)
        self.p1.deinit()
        self.p2.deinit()
        coast_pins()


def measure(seconds):
    """Return (counts, output RPM) over the given window."""
    c0 = count
    t0 = time.ticks_ms()
    time.sleep(seconds)
    dc = count - c0
    dt = time.ticks_diff(time.ticks_ms(), t0) / 1000
    return dc, dc / CPR_OUT / dt * 60
