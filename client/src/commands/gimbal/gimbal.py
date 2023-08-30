import time
import threading
from commands.gimbal.servo import Servo


class Gimbal:
    def __init__(self, timeout: float):
        self._servo_horizontal: Servo = Servo(servo_pin=23, step=3, start_angle=10)
        self._servo_vertical: Servo = Servo(servo_pin=9, min_angle=-55, max_angle=85)
        self._timeout: float = timeout
        self._start_time: float = time.time()
        self._thread: threading.Thread = threading.Thread(target=self._gimbal_thread, daemon=True)
        self._thread.start()

    def _gimbal_thread(self) -> None:
        while True:
            if time.time() - self._start_time >= self._timeout:
                self.stop()
            else:
                self._servo_horizontal.continue_movement()
                self._servo_vertical.continue_movement()
            time.sleep(0.05)

    def up(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.stop()

    def up_left(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.forward()

    def up_right(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.forward()
        self._servo_horizontal.backward()

    def down(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.stop()

    def down_left(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.forward()

    def down_right(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.backward()
        self._servo_horizontal.backward()

    def left(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.stop()
        self._servo_horizontal.forward()

    def right(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.stop()
        self._servo_horizontal.backward()

    def center(self) -> None:
        self._start_time = time.time()
        self._servo_vertical.center()
        self._servo_horizontal.center()

    def stop(self) -> None:
        self._servo_vertical.stop()
        self._servo_horizontal.stop()
