from __future__ import annotations
from typing import List, Tuple

from .token import Token
from .. import utils

class TokenAnalizer():
    def __init__(self):
        self.registered = dict()
    
    def register_identifier(self, identifier: str, sequence: List[str], callback):
        if identifier not in self.registered:
            self.registered[identifier] = list()
        self.registered[identifier].append({"sequence": sequence, "callback": callback})


    def _parse(self, tokens: List[Token]) -> List[Token]:
        tokens = list(tokens)
        for identf, data in self.registered.items():
            for pattern in data:
                sequence = pattern["sequence"]
                callback = pattern["callback"]
                i = 0
                while i < len(tokens):
                    if utils.match_at(sequence, tokens, i):
                        tokens_seq = utils.remove_range(tokens, i, len(sequence))
                        tokens.insert(i, Token(identf, callback(*tokens_seq)))
                        parsed = True
                    i += 1
        return tokens

    def parse(self, tokens: List[Token], iterout=5) -> Token:
        tokens = self._parse(tokens)
        last_len = len(tokens)
        equal_len = 0
        while len(tokens) > 1:
            tokens = self._parse(tokens)
            if len(tokens) == last_len:
                equal_len += 1
            else:
                equal_len = 0
            if equal_len > iterout:
                for x in tokens:
                    print(x)
                raise RuntimeError(f"iterout ({iterout}) exceeded.")
            last_len = len(tokens)
        return tokens[0]
