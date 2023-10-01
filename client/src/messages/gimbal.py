from messages.message import Message


class Gimbal(Message):
    TYPE: str = 'gimbal'

    def __init__(self, horizontal: float, vertical: float, center: bool = False, **kwargs):
        self.horizontal: float = horizontal
        self.vertical: float = vertical
        self.center: bool = center

    def __repr__(self) -> str:
        return f"Gimbal(horizontal={self.horizontal}, vertical={self.vertical}, center={self.center})"
