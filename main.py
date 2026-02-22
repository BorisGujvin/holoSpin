import time
import colorsys
from apa102_pi.driver import apa102
import lgpio

HALL_PIN = 14
last_time = None
running = True
restart_animation = False

chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(chip, HALL_PIN, lgpio.SET_PULL_UP)
lgpio.gpio_claim_alert(chip, HALL_PIN, lgpio.FALLING_EDGE)

def magnet_callback(chip, gpio, level, tick):
    global last_time, restart_animation
    current_time = time.time() * 1000

    if level == 0:
        if last_time is not None:
            delta = current_time - last_time
            print(f"MAGNET DETECTED | {delta:.2f} ms since last", flush=True)
        else:
            print("MAGNET DETECTED | First detection", flush=True)

        last_time = current_time
        restart_animation = True

lgpio.callback(chip, HALL_PIN, lgpio.FALLING_EDGE, magnet_callback)

NUM_LEDS = 144
BRIGHTNESS = 1
DELAY = 0.01
PAUSE_AT_ENDS = 0.1

strip = apa102.APA102(num_led=NUM_LEDS, global_brightness=BRIGHTNESS)

print("Running rainbow runner with magnet restart...", flush=True)
print("Press Ctrl+C to stop", flush=True)

def flash_white():
    [strip.set_pixel_rgb(i, 0xFFFFFF) for i in range(NUM_LEDS)]
    strip.show()
    time.sleep(0.005)
    strip.clear_strip()
    strip.show()

def run_one_cycle(start_hue):
    for i in range(NUM_LEDS):
        if restart_animation:
            return False
        strip.clear_strip()
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(start_hue, 1.0, 1.0)]
        strip.set_pixel_rgb(i, (r << 16) | (g << 8) | b)
        strip.show()
        time.sleep(DELAY)
        start_hue = (start_hue + 0.002) % 1.0

    if restart_animation:
        return False
    time.sleep(PAUSE_AT_ENDS)

    if restart_animation:
        return False

    for i in range(NUM_LEDS - 1, -1, -1):
        if restart_animation:
            return False
        strip.clear_strip()
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(start_hue, 1.0, 1.0)]
        strip.set_pixel_rgb(i, (r << 16) | (g << 8) | b)
        strip.show()
        time.sleep(DELAY)
        start_hue = (start_hue + 0.002) % 1.0

    if restart_animation:
        return False
    time.sleep(PAUSE_AT_ENDS)

    return True

try:
    hue = 0
    while running:
        completed = run_one_cycle(hue)

        if restart_animation:
            restart_animation = False

        if completed:
            hue = (hue + 0.01) % 1.0
        else:
           flash_white()

except KeyboardInterrupt:
    print("\nStopping...")
    running = False
    strip.clear_strip()
    strip.show()
    strip.cleanup()
    lgpio.gpiochip_close(chip)
