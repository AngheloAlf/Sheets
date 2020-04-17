from __future__ import annotations


class AbstractRepresentationMeta(type):
    def __str__(self):
        return f"<'{str(self.__name__)}'>"
    def __repr__(self):
        return f"<'{str(self.__name__)}'>"


class ARepresentation(metaclass=AbstractRepresentationMeta):
    def __init__(self, sequence=None, match=None):
        super().__init__()
        self._sequence = sequence
        self._match = match
    
    def __str__(self):
        return f"{self.__class__.__name__}<{str(self._match)}>"

    def __repr__(self):
        return self.__str__()

class Start(ARepresentation):
    pass
