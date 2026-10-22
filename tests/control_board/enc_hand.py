# Encoder test phase 1 — motor never driven. Turn the output shaft by hand.
import time
import enc_common as e

e.coast_pins()
e.start_decoder()
print("Phase 1 (motor OFF, driver in coast).")
print("Turn the OUTPUT shaft ONE full turn FORWARD, slowly, within 15 s ...")
for s in range(15, 0, -1):
    print("  %2d s  counts=%6d" % (s, e.count))
    time.sleep(1)
print("Hand turn: counts=%d (expect ~ +/-9600, +/-5 %%), errors=%d" % (e.count, e.errors))
