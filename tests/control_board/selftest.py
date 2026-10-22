from machine import Pin, ADC, PWM, freq
import time, os

print("Board:", os.uname().machine)
print("CPU MHz:", freq() // 1_000_000)

led = Pin("LED", Pin.OUT)
for _ in range(6):
    led.toggle(); time.sleep(0.25)
print("LED: blinked 3 times")

v = ADC(4).read_u16() * 3.3 / 65535
print("Chip temp C: %.1f" % (27 - (v - 0.706) / 0.001721))
print("VSYS V: %.2f" % (ADC(29).read_u16() * 3.3 / 65535 * 3))

pins = list(range(0, 23)) + [26, 27, 28]
fail = []
for n in pins:
    p = Pin(n, Pin.IN, Pin.PULL_UP); time.sleep_ms(2); pu = p.value()
    p = Pin(n, Pin.OUT, value=0); time.sleep_ms(1); lo = p.value()
    p.value(1); time.sleep_ms(1); hi = p.value()
    Pin(n, Pin.IN)
    ok = (pu, lo, hi) == (1, 0, 1)
    print("GP%-2d pull-up=%d out0=%d out1=%d %s" % (n, pu, lo, hi, "OK" if ok else "FAIL"))
    if not ok:
        fail.append(n)
print("GPIO:", "PASS" if not fail else "FAIL on %s" % fail)

pwm = PWM(Pin(10), freq=20000, duty_u16=32768)
print("PWM: GP10 at 20 kHz, 50 %% -> measure DC on GP10 now (expect ~1.65 V). 20 s...")
time.sleep(20)
pwm.deinit(); Pin(10, Pin.IN)
print("Done")
