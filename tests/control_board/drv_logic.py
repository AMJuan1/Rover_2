
from machine import Pin
import time
IN1, IN2 = 16, 17
in1 = Pin(IN1, Pin.OUT, value=0); in2 = Pin(IN2, Pin.OUT, value=0)
def phase(a, b, msg, s=10):
    in1.value(a); in2.value(b); print(msg); time.sleep(s)
try:
    phase(0, 0, "COAST  IN1=0 IN2=0: supply current few mA")
    phase(1, 0, "FWD    IN1=1 IN2=0: OUT1 ~ +12 V, OUT2 ~ 0 V (to GND)")
    phase(0, 1, "REV    IN1=0 IN2=1: OUT1 ~ 0 V, OUT2 ~ +12 V")
    phase(1, 1, "BRAKE  IN1=1 IN2=1: OUT1 ~ 0 V, OUT2 ~ 0 V")
finally:
    in1.value(0); in2.value(0); print("Done: COAST")
