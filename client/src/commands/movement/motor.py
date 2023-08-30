import time
from gpiozero import Motor as GpioMotor
from commands.common.direction import Direction


class Motor:
    def __init__(
            self,
            forward: int,
            backward: int,
            enable_pin: int,
    ):
        self._motor: GpioMotor = GpioMotor(
            forward=forward,
            backward=backward,
            enable=enable_pin,
        )
        self._current_direction: Direction = Direction.STOP
        self._next_direction: Direction = Direction.STOP
        self._current_speed: float = 0
        self._next_speed: float = 0

    def continue_movement(self) -> None:
        if self._next_direction == self._current_direction and self._next_speed == self._current_speed:
            return
        if (
                self._current_direction != Direction.STOP
                and self._next_direction != self._current_direction
                and self._next_direction != Direction.STOP
        ):
            self._motor.stop()
            time.sleep(0.1)

        self._set_motor_direction(self._next_direction, self._next_speed)

    def _set_motor_direction(self, direction: Direction, speed: float) -> None:
        if direction == Direction.FORWARD:
            self._motor.forward(speed)
        elif direction == Direction.BACKWARD:
            self._motor.backward(speed)
        else:
            self._motor.stop()
        self._current_speed = speed
        self._current_direction = direction

    def forward(self, speed: float) -> None:
        self._next_speed = speed
        self._next_direction = Direction.FORWARD

    def backward(self, speed: float) -> None:
        self._next_speed = speed
        self._next_direction = Direction.BACKWARD

    def stop(self) -> None:
        self._next_speed = 0
        self._next_direction = Direction.STOP

    def cleanup(self) -> None:
        self._motor.stop()
