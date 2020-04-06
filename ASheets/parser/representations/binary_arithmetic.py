from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class BinaryOp(ARepresentation):
    def __init__(self, symbol: str, left: Token, right: Token):
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{str(self.left.token)} {self.symbol} {str(self.right.token)}'


class Power(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("^", left, right)


class Divide(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("/", left, right)

class Multiply(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("*", left, right)


class Substract(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("-", left, right)

class Add(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("+", left, right)


class Concat(BinaryOp):
    def __init__(self, left: Token, right: Token):
        super().__init__("&", left, right)

