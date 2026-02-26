import config
import time

from animation.ianimation import IAnimation

class HoloSpin(IAnimation):
    columns = [
        # Колонка 0
        [(0, 0, 0)] * 6 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 7 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 18,

        # Колонка 1
        [(0, 0, 0)] * 5 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 9 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 17,

        # Колонка 2
        [(0, 0, 0)] * 3 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 13 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 15,

        # Колонка 3
        [(0, 0, 0)] * 2 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 15 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 14,

        # Колонка 4 — глаза и нос
        [(0, 0, 0)] * 8 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 2 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 3 + [
            (255, 255, 255)] * 2 + [(0, 0, 0)] * 16,

        # Колонка 5
        [(0, 0, 0)] * 8 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 2 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 3 + [
            (255, 255, 255)] * 2 + [(0, 0, 0)] * 16,

        # Колонка 6
        [(0, 0, 0)] * 2 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 15 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 14,

        # Колонка 7
        [(0, 0, 0)] * 3 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 13 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 15,

        # Колонка 8 — улыбка
        [(0, 0, 0)] * 11 + [(255, 255, 255)] * 3 + [(0, 0, 0)] * 1 + [(255, 255, 255)] * 2 + [(0, 0, 0)] * 18,

        # Колонка 9
        [(0, 0, 0)] * 12 + [(255, 255, 255)] * 5 + [(0, 0, 0)] * 18,
    ]

    def run_cycle(self):
        for column in range(config.NUM_COLUMNS):
            if self.hall.should_restart():
                return False
            self.draw_column(column)
            column_time = self.hall.get_column_time()
            if column_time:
                print(f"published column {column} . Value {self.columns[column]} . pause {column_time / 1000}", flush=True)
                time.sleep(column_time / 1000)
            else:
                print ("no time", flush=True)
                time.sleep(1)
        return True

    def on_interrupt(self):
        self.led.fill_white()

    def on_cycle_complete(self):
        while not self.hall.should_restart():
            time.sleep(0.01)

    def draw_column(self, column_index):
        if column_index >= len(self.columns):
            return

        column = self.columns[column_index]
        self.led.clear()

        for led_index, (r, g, b) in enumerate(column):
            physical_led = led_index
            self.led.set_pixel(physical_led, r, g, b)

        self.led.show()