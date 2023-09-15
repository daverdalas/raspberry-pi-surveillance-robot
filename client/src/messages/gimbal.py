from messages.message import Message


class Gimbal(Message):
    TYPE: str = 'gimbal'

    def __init__(self, horizontal: int, vertical: int, center: bool = False, **kwargs):
        self.horizontal: int = horizontal
        self.vertical: int = vertical
        self.center: bool = center

    def __repr__(self) -> str:
        return f"Gimbal(horizontal={self.horizontal}, vertical={self.vertical}, center={self.center})"
