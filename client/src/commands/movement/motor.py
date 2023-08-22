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
        self.pin_a: int = pin_a
        self.pin_b: int = pin_b
        self.frequency: int = frequency
        self.current_direction: Direction = Direction.STOP
        self.next_direction: Direction = Direction.STOP
        self.duty_cycle: float = 0
        self.next_duty_cycle: float = 0
        self.gpio: ModuleType = gpio
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.pin_a, self.gpio.OUT)
        self.gpio.setup(self.pin_b, self.gpio.OUT)
        self.gpio.setup(enable_pin, self.gpio.OUT)
        self.pwm = self.gpio.PWM(enable_pin, self.frequency)
        self.pwm.start(0)

    def continue_movement(self):
        if self.next_direction == self.current_direction and self.next_duty_cycle == self.duty_cycle:
            return
        if self.current_direction != Direction.STOP:
            self.pwm.ChangeDutyCycle(0)
            time.sleep(0.1)

        direction = self.next_direction

        pin_states: Dict[Direction, Tuple[int, int]] = {
            Direction.FORWARD: (self.gpio.HIGH, self.gpio.LOW),
            Direction.BACKWARD: (self.gpio.LOW, self.gpio.HIGH),
            Direction.STOP: (self.gpio.LOW, self.gpio.LOW)
        }

        self.gpio.output(self.pin_a, pin_states[direction][0])
        self.gpio.output(self.pin_b, pin_states[direction][1])
        self.pwm.ChangeDutyCycle(self.next_duty_cycle)
        self.duty_cycle = self.next_duty_cycle
        self.current_direction = direction

    def forward(self, duty_cycle: float):
        self.next_duty_cycle = duty_cycle
        self.next_direction = Direction.FORWARD

    def backward(self, duty_cycle: float):
        self.next_duty_cycle = duty_cycle
        self.next_direction = Direction.BACKWARD

    def stop(self):
        self.next_duty_cycle = 0
        self.next_direction = Direction.STOP

    def cleanup(self):
        self.pwm.stop()
