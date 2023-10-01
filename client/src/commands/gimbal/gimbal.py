import time
import threading
from commands.gimbal.servo import Servo


class Gimbal:
    def __init__(self, timeout: float):
        self._servo_horizontal: Servo = Servo(servo_pin=23, start_angle=10)
        self._servo_vertical: Servo = Servo(servo_pin=9, min_angle=-55, max_angle=85)
        self._timeout: float = timeout
        self._start_time: float = time.time()
        self._thread: threading.Thread = threading.Thread(target=self._gimbal_thread, daemon=True)
        self._thread.start()

    def __call__(self, horizontal: float, vertical: float, center: bool) -> None:
        self._set_servo_movement(self._servo_horizontal, horizontal, center)
        self._set_servo_movement(self._servo_vertical, vertical, center)

    def _set_servo_movement(self, servo: Servo, step: float, center: bool) -> None:
        self._start_time = time.time()
        if center:
            servo.center()

            return
        if step > 0:
            servo.forward(abs(step))

            return
        if step < 0:
            servo.backward(abs(step))

            return
        servo.stop()

    def _gimbal_thread(self) -> None:
        while True:
            if time.time() - self._start_time >= self._timeout:
                self._servo_horizontal.stop()
                self._servo_vertical.stop()
            else:
                self._servo_horizontal.continue_movement()
                self._servo_vertical.continue_movement()
            time.sleep(0.05)
