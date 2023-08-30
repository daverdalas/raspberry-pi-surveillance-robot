import time
import threading
from commands.movement.motor import Motor


class Movement:
    _REGULAR_SPEED: float = 0.25
    _REDUCED_SPEED: float = 0.065

    def __init__(self, timeout: float):
        self._motor_left: Motor = Motor(forward=20, backward=21, enable_pin=16)
        self._motor_right: Motor = Motor(forward=19, backward=26, enable_pin=13)
        self._timeout: float = timeout
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._movement_thread, daemon=True)
        self._thread.start()

    def _movement_thread(self) -> None:
        while True:
            if time.time() - self._start_time >= self._timeout:
                self._motor_left.stop()
                self._motor_right.stop()
            else:
                self._motor_left.continue_movement()
                self._motor_right.continue_movement()
            time.sleep(0.05)

    def up(self):
        self._start_time = time.time()
        self._motor_left.forward(self._REGULAR_SPEED)
        self._motor_right.forward(self._REGULAR_SPEED)

    def up_left(self):
        self._start_time = time.time()
        self._motor_left.forward(self._REDUCED_SPEED)
        self._motor_right.forward(self._REGULAR_SPEED)

    def up_right(self):
        self._start_time = time.time()
        self._motor_left.forward(self._REGULAR_SPEED)
        self._motor_right.forward(self._REDUCED_SPEED)

    def down(self):
        self._start_time = time.time()
        self._motor_left.backward(self._REGULAR_SPEED)
        self._motor_right.backward(self._REGULAR_SPEED)

    def down_left(self):
        self._start_time = time.time()
        self._motor_left.backward(self._REDUCED_SPEED)
        self._motor_right.backward(self._REGULAR_SPEED)

    def down_right(self):
        self._start_time = time.time()
        self._motor_left.backward(self._REGULAR_SPEED)
        self._motor_right.backward(self._REDUCED_SPEED)

    def left(self):
        self._start_time = time.time()
        self._motor_left.backward(self._REGULAR_SPEED)
        self._motor_right.forward(self._REGULAR_SPEED)

    def right(self):
        self._start_time = time.time()
        self._motor_left.forward(self._REGULAR_SPEED)
        self._motor_right.backward(self._REGULAR_SPEED)

    def stop(self):
        self._start_time = time.time()
        self._motor_left.stop()
        self._motor_right.stop()

    def cleanup(self):
        self._motor_left.cleanup()
        self._motor_right.cleanup()
