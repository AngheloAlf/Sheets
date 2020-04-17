from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class UnaryOperatorPre(ARepresentation): # TODO
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

class UnaryOperatorPost(ARepresentation): # TODO
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


class _BaseUnaryOp(ARepresentation):
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


class UnaryMinus(_BaseUnaryOp):
    pass
    """
    def __init__(self):
        super().__init__("-")
    pass
    """

class UnaryPlus(_BaseUnaryOp):
    pass
    """
    def __init__(self):
        super().__init__("+")
    pass
    """


class UnaryPercent(_BaseUnaryOp):
    pass
    """
    def __init__(self):
        super().__init__("%")
    pass
    """

