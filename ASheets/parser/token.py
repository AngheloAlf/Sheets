from __future__ import annotations
from typing import List
from typing import Union


class Token():
    def __init__(self, identifier: str, token: Union[str, List[Token]]):
        self.identifier: str = identifier
        self.token: Union[str, List[Token]] = token
    
    def stringify(self, deepness=0, indent=2):
        if isinstance(self.token, (list, tuple)):
            result = (" "*indent*deepness) + "<" + f"{self.identifier}:\n"
            for i in self.token:
                if isinstance(i, Token):
                    result += i.stringify(deepness+1, indent) + "\n"
                else:
                    result += (" "*indent*(deepness+1)) + str(i) + "\n"
            result += (" "*indent*deepness) + f":{self.identifier}" + ">"
            return result
        return (" "*indent*deepness) + "<" + f"{self.identifier}: {str(self.token)}" + ">"

    def __str__(self):
        return self.stringify()
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.identifier == other.identifier
        return self.identifier == other
