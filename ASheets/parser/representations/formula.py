from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class Formula(ARepresentation):
    def __init__(self, formula: Token):
        self.formula = formula
    
    def __str__(self):
        return f'={str(self.formula.token)}'
