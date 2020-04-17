from __future__ import annotations

from .abstract_representation import ARepresentation
from ..token import Token


class Reference(ARepresentation):
    pass
    """
    def __init__(self, reference: Token):
        self.reference = reference
    
    def __str__(self):
        return str(self.reference.token)
    pass
    """


class ReferenceItem(ARepresentation):
    pass
    """
    def __init__(self, reference: Token):
        self.reference = reference
    
    def __str__(self):
        return str(self.reference.token)
    pass
    """


class NamedRange(ARepresentation):
    pass
    """
    def __init__(self, reference: Token):
        self.reference = reference
    
    def __str__(self):
        return str(self.reference.token)
    pass
    """
