from __future__ import annotations

from ..tokenizer import Token


class GenericExpression():
    def __init__(self, expr: Token):
        self.expr = expr
    
    def __str__(self):
        return str(self.expr.token)
