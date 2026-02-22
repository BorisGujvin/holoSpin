from abc import ABC, abstractmethod

class IAnimation(ABC):
    """Abstract base class for all animations"""

    def __init__(self, led_strip, hall_sensor):
        self.led = led_strip
        self.hall = hall_sensor
        self.running = True

    @abstractmethod
    def run_cycle(self):
        """Run one complete animation cycle
        Returns: True if cycle completed, False if interrupted"""
        pass

    @abstractmethod
    def on_interrupt(self):
        """Called when animation is interrupted by magnet"""
        pass

    @abstractmethod
    def on_cycle_complete(self):
        """Called when a cycle completes without interruption"""
        pass

    def run(self):
        """Main animation loop"""
        try:
            while self.running:
                completed = self.run_cycle()

                if completed:
                    self.on_cycle_complete()
                else:
                    self.on_interrupt()

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.cleanup()

    def stop(self):
        self.running = False

    def cleanup(self):
        self.led.cleanup()
        self.hall.cleanup()
