from machine import Pin, PWM
import time
IN1, IN2, F = 16, 17, 20000
def drive(d1, d2, msg, s=5):
    p1.duty_u16(65535 * d1 // 100); p2.duty_u16(65535 * d2 // 100)
    print(msg); time.sleep(s)
p1 = PWM(Pin(IN1), freq=F, duty_u16=0); p2 = PWM(Pin(IN2), freq=F, duty_u16=0)
try:
    drive(0, 0, "STOP", 2)
    drive(20, 0, "FWD fast-decay 20 %: slow turn")
    drive(50, 0, "FWD fast-decay 50 %")
    drive(100, 0, "FWD 100 %: ~67 RPM output, ~0.2 A")
    drive(0, 0, "STOP", 3)
    drive(0, 50, "REV fast-decay 50 %: opposite direction")
    drive(0, 0, "STOP", 3)
    drive(100, 50, "FWD slow-decay 50 % (IN1=1, IN2=PWM 50 %)")
    drive(100, 80, "FWD slow-decay 20 % (IN2 inverted 80 %)")
    drive(100, 100, "BRAKE (both high)", 2)
finally:
    p1.duty_u16(0); p2.duty_u16(0); p1.deinit(); p2.deinit()
    Pin(IN1, Pin.OUT, value=0); Pin(IN2, Pin.OUT, value=0); print("Done: COAST")
