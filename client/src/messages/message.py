from abc import ABC, abstractmethod
import json


class Message(ABC):
    @property
    @abstractmethod
    def TYPE(self):
        pass

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)['data']
        type = data['type']
        for Subclass in cls.__subclasses__():
            if Subclass.TYPE == type:
                return Subclass(**data)
        raise ValueError(f'Unknown message type: {type}')
