from __future__ import annotations


class Token():
    def __init__(self, identifier: str, token: str):
        self._identifier: str = identifier
        self._token: str = token

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def token(self) -> str:
        return self._token


    def __str__(self):
        return f"<{self._identifier}: {self._token}>"
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self._identifier}', '{self._token}')"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self._identifier == other.identifier
        return self._identifier == other
