from hardware.hall_sensor import HallSensor
from hardware.led_strip import LEDStrip
from animation.rainbow_runner import RainbowRunner


import config

if __name__ == "__main__":
    hall = HallSensor(config.HALL_PIN)
    led = LEDStrip(config.NUM_LEDS, config.BRIGHTNESS)

    # Choose your animation here
    animation = RainbowRunner(led, hall)

    print(f"Running {animation.__class__.__name__} with magnet restart...", flush=True)
    print("Press Ctrl+C to stop", flush=True)

    animation.run()