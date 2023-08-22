from messages.message import Message


class Movement(Message):
    TYPE = 'movement'

    def __init__(self, direction: str, **kwargs):
        self._direction = direction

    def direction(self):
        return self._direction
