# Encoder test phase 2 — MOTOR TURNS. Run only after Jan confirms the motor is clamped.
import time
import enc_common as e

e.start_decoder()
d = e.Drive()
try:
    for label, cmd, duty in (("FWD 30 %", d.fwd, 30), ("FWD 60 %", d.fwd, 60), ("REV 30 %", d.rev, 30)):
        cmd(duty)
        time.sleep(1)                       # let speed settle
        counts, rpm = e.measure(5)
        print("%-9s counts=%7d  output RPM=%6.1f" % (label, counts, rpm))
        d.brake()
        time.sleep(1)
    print("Encoder errors (missed edges): %d" % e.errors)
finally:
    d.stop()
    print("Done: COAST")
