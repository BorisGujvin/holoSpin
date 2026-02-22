import time
from apa102_pi.driver import apa102

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