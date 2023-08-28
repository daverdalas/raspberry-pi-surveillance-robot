from messages.message import Message


class Stream(Message):
    TYPE: str = 'stream'

    def __init__(self, action: str, **kwargs):
        self._action: str = action

    @property
    def action(self) -> str:
        return self._action

    def is_start(self) -> bool:
        return self._action == 'start'

    def is_stop(self) -> bool:
        return self._action == 'stop'

    def __repr__(self) -> str:
        return f"Stream(action={self._action})"
