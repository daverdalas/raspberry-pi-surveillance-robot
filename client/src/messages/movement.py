from messages.message import Message


class Movement(Message):
    TYPE: str = 'movement'

    def __init__(self, direction: str, **kwargs):
        self._direction: str = direction

    @property
    def direction(self) -> str:
        return self._direction

    def __repr__(self) -> str:
        return f"Movement(direction={self._direction})"
