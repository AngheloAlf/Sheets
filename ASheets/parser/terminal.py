from __future__ import annotations

from typing import Optional


class Terminal():
    def __init__(self, name: str, other_name: Optional[str]=None):
        self._name: str = name
        self._other_name: str = name
        if other_name is not None:
            self._other_name = other_name

    @property
    def name(self):
        return self._name
    @property
    def other_name(self):
        return self._other_name

    def __str__(self):
        return self._name
    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', '{self._other_name}')"

    def __eq__(self, other):
        if isinstance(other, Terminal):
            return self._name == other._name
        if isinstance(other, str):
            return self._name == other or self._other_name == other
        return NotImplemented

    def __hash__(self):
        return hash(self.__repr__())
