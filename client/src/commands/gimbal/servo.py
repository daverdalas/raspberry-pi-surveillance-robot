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
            step: int = 2,
    ):
        self._servo = AngularServo(
            servo_pin,
            initial_angle=start_angle,
            min_pulse_width=(1.0 - correction) / 1000,
            max_pulse_width=(2.0 + correction) / 1000,
        )
        self._current_angle = start_angle
        self._start_angle = start_angle
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._current_direction = Direction.STOP
        self._step = step

    def continue_movement(self) -> None:
        if self._current_direction == Direction.FORWARD:
            self._set_angle(self._current_angle + self._step)
        elif self._current_direction == Direction.BACKWARD:
            self._set_angle(self._current_angle - self._step)

    def forward(self) -> None:
        self._current_direction = Direction.FORWARD

    def backward(self) -> None:
        self._current_direction = Direction.BACKWARD

    def center(self) -> None:
        self._set_angle(self._start_angle)

    def stop(self) -> None:
        self._servo.detach()  # Detach the servo to stop it
        self._current_direction = Direction.STOP

    def _set_angle(self, angle) -> None:
        angle = min(max(angle, self._min_angle), self._max_angle)
        if angle == self._current_angle:
            return
        print(angle)
        try:
            self._servo.angle = angle
        except PinInvalidState:
            print('PinInvalidState')  # For remote control
        self._current_angle = angle
