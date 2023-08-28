import time
import threading
from types import ModuleType
from commands.gimbal.servo import Servo


class Gimbal:
    def __init__(self, gpio: ModuleType, timeout: float):
        self._servo_horizontal: Servo = Servo(gpio=gpio, servo_pin=23)
        self._servo_vertical: Servo = Servo(gpio=gpio, servo_pin=9, min_angle=40)
        self._timeout: float = timeout
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._gimbal_thread, daemon=True)
        self._thread.start()

    def _gimbal_thread(self):
        while True:
            if time.time() - self._start_time >= self._timeout:
                self.stop()
            else:
                self._servo_horizontal.continue_movement()
                self._servo_vertical.continue_movement()
            time.sleep(0.1)

    def up(self):
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.stop()

    def up_left(self):
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.forward()

    def up_right(self):
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.backward()

    def down(self):
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.stop()

    def down_left(self):
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.forward()

    def down_right(self):
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.backward()

    def left(self):
        self._start_time = time.time()
        self._servo_vertical.stop()
        self._servo_horizontal.forward()

    def right(self):
        self._start_time = time.time()
        self._servo_vertical.stop()
        self._servo_horizontal.backward()

    def center(self):
        self._servo_vertical.center()
        self._servo_horizontal.center()

    def stop(self):
        self._servo_vertical.stop()
        self._servo_horizontal.stop()

    def cleanup(self):
        self._servo_horizontal.cleanup()
        self._servo_vertical.cleanup()
