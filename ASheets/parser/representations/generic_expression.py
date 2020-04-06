from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class GenericExpression(ARepresentation):
    def __init__(self, expr: Token):
        self.expr = expr
    
    def __str__(self):
        return str(self.expr.token)
