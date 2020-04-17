from __future__ import annotations
from typing import Optional

from .abstract_representation import ARepresentation
from ..token import Token


class Identifier(ARepresentation):
    pass
    """
    def __init__(self, identf: Token, extra: Optional[Token]=None):
        self.identf = identf
        self.extra = extra
    
    def __str__(self):
        if self.extra is None:
            return str(self.identf.token)
        return str(self.identf.token)+str(self.extra.token)
    pass
    """
