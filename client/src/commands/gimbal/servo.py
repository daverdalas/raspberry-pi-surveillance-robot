from gpiozero import AngularServo
from commands.common.direction import Direction


class Servo:
    def __init__(self, servo_pin, min_angle=0, max_angle=180, start_angle=85):
        self._servo = AngularServo(servo_pin, min_angle=min_angle, max_angle=max_angle, initial_angle=start_angle)
        self._current_angle = start_angle
        self._start_angle = start_angle
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._current_direction = Direction.STOP

    def continue_movement(self):
        if self._current_direction == Direction.FORWARD:
            self._set_angle(self._current_angle + 4)
        elif self._current_direction == Direction.BACKWARD:
            self._set_angle(self._current_angle - 4)

    def forward(self):
        self._current_direction = Direction.FORWARD

    def backward(self):
        self._current_direction = Direction.BACKWARD

    def center(self):
        self._set_angle(self._start_angle)

    def stop(self):
        self._servo.detach()  # Detach the servo to stop it
        self._current_direction = Direction.STOP

    def _set_angle(self, angle):
        angle = min(max(angle, self._min_angle), self._max_angle)
        self._servo.angle = angle
        self._current_angle = angle

    def cleanup(self):
        # Detaching the servo when done
        self._servo.detach()
