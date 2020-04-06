from __future__ import annotations
from typing import Optional

from ..tokenizer import Token


class Identifier():
    def __init__(self, identf: Token, extra: Optional[Token]=None):
        self.identf = identf
        self.extra = extra
    
    def __str__(self):
        if self.extra is None:
            return str(self.identf.token)
        return str(self.identf.token)+str(self.extra.token)
