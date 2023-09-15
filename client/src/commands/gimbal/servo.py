from gpiozero import AngularServo
from gpiozero.exc import PinInvalidState
from commands.common.direction import Direction


class Servo:
    def __init__(
            self,
            servo_pin,
            min_angle: int = -90,
            max_angle: int = 90,
            start_angle: int = 0,
            correction: float = 0.45,
    ):
        self._step = None
        self._servo: AngularServo = AngularServo(
            pin=servo_pin,
            initial_angle=start_angle,
            min_pulse_width=(1.0 - correction) / 1000,
            max_pulse_width=(2.0 + correction) / 1000,
        )
        self._current_angle: float = start_angle
        self._start_angle: int = start_angle
        self._min_angle: int = min_angle
        self._max_angle: int = max_angle
        self._current_direction: Direction = Direction.STOP

    def continue_movement(self) -> None:
        if self._current_direction == Direction.FORWARD:
            self._set_angle(self._current_angle + self._step)
        elif self._current_direction == Direction.BACKWARD:
            self._set_angle(self._current_angle - self._step)

    def forward(self, step: int) -> None:
        self._step = step
        self._current_direction = Direction.FORWARD

    def backward(self, step: int) -> None:
        self._step = step
        self._current_direction = Direction.BACKWARD

    def center(self) -> None:
        self._set_angle(self._start_angle)

    def stop(self) -> None:
        self._current_direction = Direction.STOP

    def _set_angle(self, angle) -> None:
        angle = min(max(angle, self._min_angle), self._max_angle)
        if angle == self._current_angle:
            return
        try:
            self._servo.angle = angle
        except PinInvalidState:
            print('PinInvalidState')  # For remote control
        self._current_angle = angle
