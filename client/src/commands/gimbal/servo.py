import time
from types import ModuleType
from commands.common.direction import Direction


class Servo:
    _ANGLE_INCREMENT = 2
    _PWM_DUTY_CYCLE_OFFSET = 2.5
    _ANGLE_TO_DUTY_CYCLE_RATIO = 18

    def __init__(
            self,
            gpio: ModuleType,
            servo_pin: int,
            start_angle: int = 85,
            frequency: int = 50,
            min_angle: int = 0,
            max_angle: int = 180
    ):
        self._initialize_gpio(gpio, servo_pin, frequency)
        self._start_angle = start_angle
        self._current_angle = start_angle
        self._max_angle = max_angle
        self._min_angle = min_angle
        self.center()
        time.sleep(0.2)
        self._current_direction = Direction.STOP
        self._pwm.ChangeDutyCycle(0)

    def _initialize_gpio(self, gpio, servo_pin, frequency):
        gpio.setmode(gpio.BCM)
        gpio.setup(servo_pin, gpio.OUT)
        self._pwm = gpio.PWM(servo_pin, frequency)
        self._pwm.start(0)

    def continue_movement(self):
        if self._current_direction == Direction.FORWARD:
            self._set_angle(self._current_angle + self._ANGLE_INCREMENT)
        elif self._current_direction == Direction.BACKWARD:
            self._set_angle(self._current_angle - self._ANGLE_INCREMENT)

    def forward(self):
        self._current_direction = Direction.FORWARD

    def backward(self):
        self._current_direction = Direction.BACKWARD

    def center(self):
        self._set_angle(self._start_angle)

    def stop(self):
        self._pwm.ChangeDutyCycle(0)
        self._current_direction = Direction.STOP

    def cleanup(self):
        self._pwm.stop()

    def _set_angle(self, angle: int):
        angle = min(max(angle, self._min_angle), self._max_angle)
        duty_cycle = angle / self._ANGLE_TO_DUTY_CYCLE_RATIO + self._PWM_DUTY_CYCLE_OFFSET
        self._pwm.ChangeDutyCycle(duty_cycle)
        self._current_angle = angle
