from typing import Tuple, Dict
from types import ModuleType
import time
from commands.common.direction import Direction


class Motor:
    def __init__(
            self,
            gpio: ModuleType,
            pin_a: int,
            pin_b: int,
            enable_pin: int,
            frequency: int = 2000
    ):
        self._pin_a: int = pin_a
        self._pin_b: int = pin_b
        self._frequency: int = frequency
        self._current_direction: Direction = Direction.STOP
        self._next_direction: Direction = Direction.STOP
        self._duty_cycle: float = 0
        self._next_duty_cycle: float = 0
        self._gpio: ModuleType = gpio
        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setup(self._pin_a, self._gpio.OUT)
        self._gpio.setup(self._pin_b, self._gpio.OUT)
        self._gpio.setup(enable_pin, self._gpio.OUT)
        self._pwm = self._gpio.PWM(enable_pin, self._frequency)
        self._pwm.start(0)

    def _set_motor_direction(self, direction: Direction, duty_cycle: float) -> None:
        pin_states: Dict[Direction, Tuple[int, int]] = {
            Direction.FORWARD: (self._gpio.HIGH, self._gpio.LOW),
            Direction.BACKWARD: (self._gpio.LOW, self._gpio.HIGH),
            Direction.STOP: (self._gpio.LOW, self._gpio.LOW)
        }
        self._gpio.output(self._pin_a, pin_states[direction][0])
        self._gpio.output(self._pin_b, pin_states[direction][1])
        self._pwm.ChangeDutyCycle(duty_cycle)
        self._duty_cycle = duty_cycle
        self._current_direction = direction

    def continue_movement(self) -> None:
        if self._next_direction == self._current_direction and self._next_duty_cycle == self._duty_cycle:
            return
        if self._current_direction != Direction.STOP:
            self._pwm.ChangeDutyCycle(0)
            time.sleep(0.1)

        self._set_motor_direction(self._next_direction, self._next_duty_cycle)

    def forward(self, duty_cycle: float) -> None:
        self._next_duty_cycle = duty_cycle
        self._next_direction = Direction.FORWARD

    def backward(self, duty_cycle: float) -> None:
        self._next_duty_cycle = duty_cycle
        self._next_direction = Direction.BACKWARD

    def stop(self) -> None:
        self._next_duty_cycle = 0
        self._next_direction = Direction.STOP

    def cleanup(self) -> None:
        self._pwm.stop()
