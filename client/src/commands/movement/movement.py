import time
import threading
from commands.movement.motor import Motor
from types import ModuleType


class Movement:
    DUTY_CYCLE: int = 50
    REDUCED_DUTY_CYCLE: int = 1

    def __init__(self, gpio: ModuleType, timeout: float):
        self._motor_left: Motor = Motor(gpio=gpio, pin_a=20, pin_b=21, enable_pin=16)
        self._motor_right: Motor = Motor(gpio=gpio, pin_a=19, pin_b=26, enable_pin=13)
        self._timeout: float = timeout
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._movement_thread, daemon=True)
        self._thread.start()

    def _movement_thread(self):
        while True:
            if time.time() - self._start_time >= self._timeout:
                self.stop()
            else:
                self._motor_left.continue_movement()
                self._motor_right.continue_movement()
            time.sleep(0.1)

    def up(self):
        self._start_time = time.time()
        self._motor_left.forward(self.DUTY_CYCLE)
        self._motor_right.forward(self.DUTY_CYCLE)

    def up_left(self):
        self._start_time = time.time()
        self._motor_left.forward(self.REDUCED_DUTY_CYCLE)
        self._motor_right.forward(self.DUTY_CYCLE)

    def up_right(self):
        self._start_time = time.time()
        self._motor_left.forward(self.DUTY_CYCLE)
        self._motor_right.forward(self.REDUCED_DUTY_CYCLE)

    def down(self):
        self._start_time = time.time()
        self._motor_left.backward(self.DUTY_CYCLE)
        self._motor_right.backward(self.DUTY_CYCLE)

    def down_left(self):
        self._start_time = time.time()
        self._motor_left.backward(self.REDUCED_DUTY_CYCLE)
        self._motor_right.backward(self.DUTY_CYCLE)

    def down_right(self):
        self._start_time = time.time()
        self._motor_left.backward(self.DUTY_CYCLE)
        self._motor_right.backward(self.REDUCED_DUTY_CYCLE)

    def left(self):
        self._start_time = time.time()
        self._motor_left.backward(self.DUTY_CYCLE)
        self._motor_right.forward(self.DUTY_CYCLE)

    def right(self):
        self._start_time = time.time()
        self._motor_left.forward(self.DUTY_CYCLE)
        self._motor_right.backward(self.DUTY_CYCLE)

    def stop(self):
        self._motor_left.stop()
        self._motor_right.stop()

    def cleanup(self):
        self.stop()
        self._motor_left.cleanup()
        self._motor_right.cleanup()
