import lgpio
import time
class HallSensor:
    def __init__(self, pin):
        self.pin = pin
        self.last_time = None
        self.restart_requested = False

        self.chip = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_input(self.chip, self.pin, lgpio.SET_PULL_UP)
        lgpio.gpio_claim_alert(self.chip, self.pin, lgpio.FALLING_EDGE)
        lgpio.callback(self.chip, self.pin, lgpio.FALLING_EDGE, self._callback)

    def _callback(self, chip, gpio, level, tick):
        current_time = time.time() * 1000

        if level == 0:
            if self.last_time is not None:
                delta = current_time - self.last_time
                print(f"MAGNET DETECTED | {delta:.2f} ms since last", flush=True)
            else:
                print("MAGNET DETECTED | First detection", flush=True)

            self.last_time = current_time
            self.restart_requested = True

    def should_restart(self):
        if self.restart_requested:
            self.restart_requested = False
            return True
        return False

    def cleanup(self):
        lgpio.gpiochip_close(self.chip)
