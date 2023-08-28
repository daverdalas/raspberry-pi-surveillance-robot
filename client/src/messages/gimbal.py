from messages.message import Message


class Gimbal(Message):
    TYPE: str = 'gimbal'

    def __init__(self, direction: str, **kwargs):
        self._direction: str = direction

    @property
    def direction(self) -> str:
        return self._direction

    def __repr__(self) -> str:
        return f"Gimbal(direction={self._direction})"