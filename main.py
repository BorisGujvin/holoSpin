import time
import colorsys
from apa102_pi.driver import apa102
import lgpio

HALL_PIN = 14
NUM_LEDS = 144
BRIGHTNESS = 1
DELAY = 0.01
PAUSE_AT_ENDS = 0.1


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


class LEDStrip:
    def __init__(self, num_leds, brightness):
        self.num_leds = num_leds
        self.strip = apa102.APA102(num_led=num_leds, global_brightness=brightness)

    def clear(self):
        self.strip.clear_strip()
        self.strip.show()

    def set_pixel(self, index, r, g, b):
        self.strip.set_pixel_rgb(index, (r << 16) | (g << 8) | b)

    def show(self):
        self.strip.show()

    def fill_white(self, duration=0.005):
        for i in range(self.num_leds):
            self.set_pixel(i, 255, 255, 255)
        self.show()
        time.sleep(duration)
        self.clear()
        self.show()

    def cleanup(self):
        self.clear()
        self.strip.cleanup()


class Animation:
    def __init__(self, led_strip, hall_sensor):
        self.led = led_strip
        self.hall = hall_sensor
        self.hue = 0
        self.running = True

    def _get_color(self):
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)]
        return r, g, b

    def _step_hue(self):
        self.hue = (self.hue + 0.002) % 1.0

    def _forward_pass(self):
        for i in range(NUM_LEDS):
            if self.hall.should_restart():
                return False
            self.led.clear()
            r, g, b = self._get_color()
            self.led.set_pixel(i, r, g, b)
            self.led.show()
            time.sleep(DELAY)
            self._step_hue()
        return True

    def _backward_pass(self):
        for i in range(NUM_LEDS - 1, -1, -1):
            if self.hall.should_restart():
                return False
            self.led.clear()
            r, g, b = self._get_color()
            self.led.set_pixel(i, r, g, b)
            self.led.show()
            time.sleep(DELAY)
            self._step_hue()
        return True

    def _pause(self):
        if self.hall.should_restart():
            return False
        time.sleep(PAUSE_AT_ENDS)
        return not self.hall.should_restart()

    def run_cycle(self):
        """Run one full cycle with possible interruption"""
        if not self._forward_pass():
            return False
        if not self._pause():
            return False
        if not self._backward_pass():
            return False
        if not self._pause():
            return False
        return True

    def run(self):
        """Main animation loop"""
        try:
            while self.running:
                completed = self.run_cycle()

                if completed:
                    # Cycle completed without interruption - shift base color
                    self.hue = (self.hue + 0.01) % 1.0
                else:
                    # Interrupted by magnet - flash white
                    self.led.fill_white()

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.cleanup()

    def stop(self):
        self.running = False

    def cleanup(self):
        self.led.cleanup()
        self.hall.cleanup()


# ============== MAIN ==============
if __name__ == "__main__":
    hall = HallSensor(HALL_PIN)
    led = LEDStrip(NUM_LEDS, BRIGHTNESS)
    animation = Animation(led, hall)

    print("Running rainbow runner with magnet restart...", flush=True)
    print("Press Ctrl+C to stop", flush=True)

    animation.run()