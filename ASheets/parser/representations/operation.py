from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class Operation(ARepresentation): # TODO
    pass
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None
    
    def __str__(self):
        return f'{str(self.left.token)} {self.symbol} {str(self.right.token)}'
    pass
    """

class OperationItem(ARepresentation): # TODO
    pass
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None
    
    def __str__(self):
        return f'{str(self.left.token)} {self.symbol} {str(self.right.token)}'
    pass
    """

