from __future__ import annotations
from typing import Optional

from .abstract_representation import ARepresentation
from ..token import Token


class Param(ARepresentation):
    pass
    """
    def __init__(self, expr: Token):
        self.expr = expr
    
    def __str__(self):
        return str(self.expr.token) + ", "
    pass
    """


class Params(ARepresentation):
    pass
    """
    def __init__(self, param: Token, other_params: Optional[Token]=None):
        self.param = param
        self.other_params = other_params
    
    def __str__(self):
        if self.other_params is None:
            return "(" + str(self.param.token)
        return str(self.other_params.token) + str(self.param.token)
    pass
    """


class ParamList(ARepresentation):
    pass
    """
    def __init__(self, params: Token, expr: Token):
        self.params = params
        self.expr = expr
    
    def __str__(self):
        return str(self.params.token) + str(self.expr.token) + ")"
    pass
    """


class FuncCall(ARepresentation):
    pass
    """
    def __init__(self, name: Token, param: Optional[Token]=None, param_list: Optional[Token]=None):
        self.name = name
        self.param = param
        self.param_list = param_list
    
    def __str__(self):
        if self.param is not None:
            return f"{str(self.name.token)}({str(self.param.token)})"
        if self.param_list is not None:
            return f"{str(self.name.token)}{str(self.param_list.token)}"
        return f"{str(self.name.token)}()"
    pass
    """
