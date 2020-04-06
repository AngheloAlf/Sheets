from __future__ import annotations

from ..tokenizer import Token


class CompBase():
    def __init__(self, symbol: str, left: Token, right: Token):
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __str__(self):
        return f'{str(self.left.token)}{self.symbol}{str(self.right.token)}'


class Equal(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__("=", left, right)

class NotEqual(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__("<>", left, right)


class LessEqual(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__("<=", left, right)

class GreaterEqual(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__(">=", left, right)


class LessThan(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__("<", left, right)

class GreaterThan(CompBase):
    def __init__(self, left: Token, right: Token):
        super().__init__(">", left, right)

