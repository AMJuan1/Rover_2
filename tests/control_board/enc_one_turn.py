# Encoder CPR check without hand-turning (gearbox self-locks) — MOTOR TURNS.
# Mark the output shaft/hub, run: the motor drives forward slowly until the encoder reports
# one output revolution (9,600 counts) and brakes. The mark must be back at its start.
import time
import enc_common as e

DUTY = 25                    # % slow decay; steady from ~20 %
TIMEOUT_S = 20               # ~1 rev at 25 % takes a few seconds

e.start_decoder()
d = e.Drive()
try:
    d.fwd(DUTY)
    t0 = time.ticks_ms()
    while abs(e.count) < e.CPR_OUT:
        if time.ticks_diff(time.ticks_ms(), t0) > TIMEOUT_S * 1000:
            print("TIMEOUT: only %d counts after %d s (encoder wiring?)" % (e.count, TIMEOUT_S))
            break
    d.brake()
    t_run = time.ticks_diff(time.ticks_ms(), t0) / 1000
    at_brake = e.count
    time.sleep(1)
    print("Counts at brake=%d, after stop=%d (overshoot %d), %.1f s, errors=%d"
          % (at_brake, e.count, e.count - at_brake, t_run, e.errors))
    print("Sign: %s (forward should be positive; if negative, swap yellow/white)"
          % ("positive" if e.count > 0 else "NEGATIVE"))
    print("Check the mark: it should be back at its start (one output turn).")
finally:
    d.stop()
    print("Done: COAST")
