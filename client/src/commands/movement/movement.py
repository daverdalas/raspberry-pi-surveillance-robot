import time
import threading
from commands.movement.motor import Motor
from types import ModuleType


class Movement:
    DUTY_CYCLE: int = 50
    REDUCED_DUTY_CYCLE: int = 1

    def __init__(self, gpio: ModuleType, timeout: float):
        self.motor_left: Motor = Motor(gpio=gpio, pin_a=20, pin_b=21, enable_pin=16)
        self.motor_right: Motor = Motor(gpio=gpio, pin_a=19, pin_b=26, enable_pin=13)
        self.timeout: float = timeout
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._movement_thread, daemon=True)
        self.thread.start()

    def _movement_thread(self):
        while True:
            if time.time() - self.start_time >= self.timeout:
                self.motor_left.stop()
                self.motor_right.stop()
            else:
                self.motor_left.continue_movement()
                self.motor_right.continue_movement()
            time.sleep(0.1)

    def up(self):
        self.start_time = time.time()
        self.motor_left.forward(self.DUTY_CYCLE)
        self.motor_right.forward(self.DUTY_CYCLE)

    def up_left(self):
        self.start_time = time.time()
        self.motor_left.forward(self.REDUCED_DUTY_CYCLE)
        self.motor_right.forward(self.DUTY_CYCLE)

    def up_right(self):
        self.start_time = time.time()
        self.motor_left.forward(self.DUTY_CYCLE)
        self.motor_right.forward(self.REDUCED_DUTY_CYCLE)

    def down(self):
        self.start_time = time.time()
        self.motor_left.backward(self.DUTY_CYCLE)
        self.motor_right.backward(self.DUTY_CYCLE)

    def down_left(self):
        self.start_time = time.time()
        self.motor_left.backward(self.REDUCED_DUTY_CYCLE)
        self.motor_right.backward(self.DUTY_CYCLE)

    def down_right(self):
        self.start_time = time.time()
        self.motor_left.backward(self.DUTY_CYCLE)
        self.motor_right.backward(self.REDUCED_DUTY_CYCLE)

    def left(self):
        self.start_time = time.time()
        self.motor_left.backward(self.DUTY_CYCLE)
        self.motor_right.forward(self.DUTY_CYCLE)

    def right(self):
        self.start_time = time.time()
        self.motor_left.forward(self.DUTY_CYCLE)
        self.motor_right.backward(self.DUTY_CYCLE)

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def cleanup(self):
        self.stop()
        self.motor_left.cleanup()
        self.motor_right.cleanup()
