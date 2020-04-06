
from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class A1(ARepresentation):
    def __init__(self, column: Token, row: Token, fixed_col: bool=False, fixed_row: bool=False):
        self.column = column
        self.row = row
        self.fixed_col = fixed_col
        self.fixed_row = fixed_row
    
    def __str__(self):
        result = ""
        if self.fixed_col:
            result += "$"
        result += str(self.column.token)
        if self.fixed_row:
            result += "$"
        result += str(self.row.token)
        return result


class A1_A1(ARepresentation):
    def __init__(self, from_: Token, to_: Token):
        self.from_ = from_
        self.to_ = to_
    
    def __str__(self):
        return f"{self.from_.token}:{self.to_.token}"


class Sheet_A1(ARepresentation):
    def __init__(self, sheet_name: Token, a1: Token):
        self.sheet_name = sheet_name
        self.a1 = a1
    
    def __str__(self):
        return f"{self.sheet_name.token}!{self.a1.token}"
