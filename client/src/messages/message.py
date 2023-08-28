from abc import ABC, abstractmethod
import json


class Message(ABC):

    @property
    @abstractmethod
    def TYPE(self) -> str:
        """Return the type of the message"""
        pass

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        data = json.loads(json_str)['data']
        type_ = data.get('type', '')
        for Subclass in cls.__subclasses__():
            if Subclass.TYPE == type_:
                return Subclass(**data)
        raise ValueError(f'Unknown message type: {type_}')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.TYPE})"