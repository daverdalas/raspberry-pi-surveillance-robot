from messages.message import Message


class Stream(Message):
    TYPE: str = 'stream'

    def __init__(self, action: str, **kwargs):
        self.action: str = action

    def is_start(self) -> bool:
        return self.action == 'start'

    def is_stop(self) -> bool:
        return self.action == 'stop'

    def __repr__(self) -> str:
        return f"Stream(action={self.action})"
