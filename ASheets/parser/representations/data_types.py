from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class TypeString(ARepresentation):
    pass
    """
    def __init__(self, string: Token):
        self.string = string
    
    def __str__(self):
        return f'"{str(self.string.token)}"'
    pass
    """


class TypeNumber(ARepresentation):
    pass
    """
    def __init__(self, number: Token):
        self.number = number
    
    def __str__(self):
        return str(self.number.token)
    pass
    """


class TypeBoolean(ARepresentation):
    pass
    """
    def __init__(self, boolean: Token):
        self.boolean = boolean
    
    def __str__(self):
        return str(self.boolean.token)
    pass
    """


class TypeErrorGeneral(ARepresentation):
    pass
    """
    def __init__(self, error: Token):
        self.error = error
    
    def __str__(self):
        return str(self.error.token)
    pass
    """


class Constant(ARepresentation):
    pass
    """
    def __init__(self, constant: Token):
        self.constant = constant
    
    def __str__(self):
        return str(self.constant.token)
    pass
    """
