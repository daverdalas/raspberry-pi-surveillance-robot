import time
import threading
from types import ModuleType
from commands.gimbal.servo import Servo


class Gimbal:
    def __init__(self, gpio: ModuleType, timeout: float):
        self.servo_horizontal: Servo = Servo(gpio=gpio, servo_pin=23)
        self.servo_vertical: Servo = Servo(gpio=gpio, servo_pin=9, min_angle=40)
        self.timeout: float = timeout
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._gimbal_thread, daemon=True)
        self.thread.start()

    def _gimbal_thread(self):
        while True:
            if time.time() - self.start_time >= self.timeout:
                self.servo_horizontal.stop()
                self.servo_vertical.stop()
            else:
                self.servo_horizontal.continue_movement()
                self.servo_vertical.continue_movement()
            time.sleep(0.1)

    def up(self):
        self.start_time = time.time()
        self.servo_vertical.forward()
        self.servo_horizontal.stop()

    def up_left(self):
        self.start_time = time.time()
        self.servo_vertical.forward()
        self.servo_horizontal.forward()

    def up_right(self):
        self.start_time = time.time()
        self.servo_vertical.forward()
        self.servo_horizontal.backward()

    def down(self):
        self.start_time = time.time()
        self.servo_vertical.backward()
        self.servo_horizontal.stop()

    def down_left(self):
        self.start_time = time.time()
        self.servo_vertical.backward()
        self.servo_horizontal.forward()

    def down_right(self):
        self.start_time = time.time()
        self.servo_vertical.backward()
        self.servo_horizontal.backward()

    def left(self):
        self.start_time = time.time()
        self.servo_vertical.stop()
        self.servo_horizontal.forward()

    def right(self):
        self.start_time = time.time()
        self.servo_vertical.stop()
        self.servo_horizontal.backward()

    def center(self):
        self.servo_vertical.center()
        self.servo_horizontal.center()

    def stop(self):
        self.servo_vertical.stop()
        self.servo_horizontal.stop()

    def cleanup(self):
        self.servo_horizontal.cleanup()
        self.servo_vertical.cleanup()
