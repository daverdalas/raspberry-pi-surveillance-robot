from messages.message import Message


class Movement(Message):
    TYPE: str = 'movement'

    def __init__(self, left: float, right: float, **kwargs):
        self.left: float = left
        self.right: float = right

    def __repr__(self) -> str:
        return f"Movement(left={self.left}) right={self.right})"
