import config
import colorsys
import time
from animation.ianimation import IAnimation

class RainbowRunner(IAnimation):
    """Original animation: forward -> pause -> backward -> pause"""

    def __init__(self, led_strip, hall_sensor):
        super().__init__(led_strip, hall_sensor)
        self.hue = 0
        self.delay = config.DELAY
        self.pause_duration = config.PAUSE_AT_ENDS

    def _get_color(self):
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)]
        return r, g, b

    def _step_hue(self):
        self.hue = (self.hue + 0.002) % 1.0

    def _forward_pass(self):
        for i in range(config.NUM_LEDS):
            if self.hall.should_restart():
                return False
            self.led.clear()
            r, g, b = self._get_color()
            self.led.set_pixel(i, r, g, b)
            self.led.show()
            time.sleep(self.delay)
            self._step_hue()
        return True

    def _backward_pass(self):
        for i in range(config.NUM_LEDS - 1, -1, -1):
            if self.hall.should_restart():
                return False
            self.led.clear()
            r, g, b = self._get_color()
            self.led.set_pixel(i, r, g, b)
            self.led.show()
            time.sleep(self.delay)
            self._step_hue()
        return True

    def _pause(self):
        if self.hall.should_restart():
            return False
        time.sleep(self.pause_duration)
        return not self.hall.should_restart()

    def run_cycle(self):
        if not self._forward_pass():
            return False
        if not self._pause():
            return False
        if not self._backward_pass():
            return False
        if not self._pause():
            return False
        return True

    def on_interrupt(self):
        self.led.fill_white()

    def on_cycle_complete(self):
        self.hue = (self.hue + 0.01) % 1.0
