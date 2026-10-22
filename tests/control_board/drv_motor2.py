

from machine import Pin, PWM
import time
IN1, IN2, F = 16, 17, 20000
p1 = PWM(Pin(IN1), freq=F, duty_u16=0); p2 = PWM(Pin(IN2), freq=F, duty_u16=0)
def set_duty(d1, d2):
    p1.duty_u16(65535 * d1 // 100); p2.duty_u16(65535 * d2 // 100)
def fwd(d):   # slow decay forward: IN1 high, IN2 PWM inverted
    set_duty(100, 100 - d)
def rev(d):   # slow decay reverse: IN2 high, IN1 PWM inverted
    set_duty(100 - d, 100)
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
