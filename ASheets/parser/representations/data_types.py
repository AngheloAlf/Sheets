from __future__ import annotations

from ..tokenizer import Token


class TypeString():
    def __init__(self, string: Token):
        self.string = string
    
    def __str__(self):
        return f'"{str(self.string.token)}"'


class TypeFloat():
    def __init__(self, before_dot: Token, after_dot: Token):
        self.before_dot = before_dot
        self.after_dot = after_dot
    
    def __str__(self):
        return f"{str(self.before_dot.token)}.{str(self.after_dot.token)}"
