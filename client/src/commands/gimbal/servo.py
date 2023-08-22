import time
from types import ModuleType

from commands.common.direction import Direction


class Servo:
    def __init__(
            self,
            gpio: ModuleType,
            servo_pin: int,
            start_angle: int = 85,
            frequency: int = 50,
            min_angle: int = 0,
            max_angle: int = 180
    ):
        gpio.setmode(gpio.BCM)
        gpio.setup(servo_pin, gpio.OUT)
        self.pwm = gpio.PWM(servo_pin, frequency)
        self.pwm.start(0)
        self.start_angle: int = start_angle
        self.current_angle: int = start_angle
        self.max_angle: int = max_angle
        self.min_angle: int = min_angle
        self.center()
        time.sleep(0.2)
        self.current_direction: Direction = Direction.STOP
        self.pwm.ChangeDutyCycle(0)

    def continue_movement(self):
        if self.current_direction == Direction.FORWARD:
            self._set_angle(self.current_angle + 2)
        if self.current_direction == Direction.BACKWARD:
            self._set_angle(self.current_angle - 2)

    def forward(self):
        self.current_direction = Direction.FORWARD

    def backward(self):
        self.current_direction = Direction.BACKWARD

    def center(self):
        self._set_angle(self.start_angle)

    def stop(self):
        if self.current_direction != Direction.STOP:
            self.pwm.ChangeDutyCycle(0)
            self.current_direction = Direction.STOP

    def cleanup(self):
        self.pwm.stop()

    def _set_angle(self, angle: int):
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle
        duty_cycle = angle / 18 + 2.5
        self.pwm.ChangeDutyCycle(duty_cycle)
        self.current_angle = angle
