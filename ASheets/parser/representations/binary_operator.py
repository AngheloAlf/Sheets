from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class BinaryOperator(ARepresentation): # TODO
    pass
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None
    
    def __str__(self):
        return f'{str(self.left.token)} {self.symbol} {str(self.right.token)}'
    """


class BaseBinaryOp(ARepresentation):
    pass
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.left = None
        self.right = None
    
    def __str__(self):
        return f'{str(self.left.token)} {self.symbol} {str(self.right.token)}'
    """


class Power(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("^")
    """


class Divide(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("/")
    """

class Multiply(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("*")
    """


class Substract(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("-")
    """

class Add(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("+")
    """


class Concat(BaseBinaryOp):
    pass
    """
    def __init__(self):
        super().__init__("&")
    """




class Equal(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__("=")
    """

class NotEqual(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__("<>")
    """


class LessEqual(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__("<=")
    """

class GreaterEqual(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__(">=")
    """


class LessThan(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__("<")
    """

class GreaterThan(BaseBinaryOp):
    pass
    """
    def __init__(self, left: Token, right: Token):
        super().__init__(">")
    """

