from __future__ import annotations

from ..tokenizer import Token


class Formula():
    def __init__(self, formula: Token):
        self.formula = formula
    
    def __str__(self):
        return f'={str(self.formula.token)}'
