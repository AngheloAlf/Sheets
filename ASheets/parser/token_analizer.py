from __future__ import annotations
from typing import List, Tuple

from .tokenizer import Token
from .. import utils


class TokenAnalizer():
    def __init__(self):
        self.registered = dict()
    
    def register_identifier(self, identifier: str, sequence: List[str], callback):
        if identifier not in self.registered:
            self.registered[identifier] = list()
        self.registered[identifier].append({"sequence": sequence, "callback": callback})


    def _parse(self, tokens: List[Token]):
        tokens = list(tokens)
            # tok = tokens[i]

            #parsed = False
        for identf, data in self.registered.items():
            for pattern in data:
                sequence = pattern["sequence"]
                callback = pattern["callback"]
                i = 0
                while i < len(tokens):
                    if utils.match_at(sequence, tokens, i):
                        # print(identf)
                        tokens_seq = utils.remove_range(tokens, i, len(sequence))
                        tokens.insert(i, Token(identf, callback(*tokens_seq)))
                        parsed = True
                        # print("\t", tok)
                    i += 1
                    #if parsed:
                    #    break
                #if parsed:
                #    break
        
        return tokens

    def parse(self, tokens, iterout=5):
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



analizer = TokenAnalizer()

analizer.register_identifier("A1", ["WORD", "$", "NUMBER"], lambda *x: x)
analizer.register_identifier("A1", ["$", "WORD", "NUMBER"], lambda *x: x)
analizer.register_identifier("A1", ["$", "WORD", "$", "NUMBER"], lambda *x: x)

analizer.register_identifier("STRING", ["SINGLE_QUOTE_STRING"], lambda *x: x)
analizer.register_identifier("STRING", ["DOUBLE_QUOTE_STRING"], lambda *x: x)

analizer.register_identifier("FLOAT", ["NUMBER", ".", "NUMBER"], lambda *x: x)

analizer.register_identifier("IDENTIFIER", ["WORD", "NUMBER"], lambda *x: x)
analizer.register_identifier("IDENTIFIER", ["WORD"], lambda *x: x)

analizer.register_identifier("A1:A1", ["A1", ":", "A1"], lambda *x: x)
analizer.register_identifier("A1:A1", ["A1", ":", "IDENTIFIER"], lambda *x: x)
analizer.register_identifier("A1:A1", ["IDENTIFIER", ":", "A1"], lambda *x: x)

analizer.register_identifier("SHEET!A1", ["IDENTIFIER", "!", "A1"], lambda *x: x)
analizer.register_identifier("SHEET!A1:A1", ["IDENTIFIER", "!", "A1:A1"], lambda *x: x)

analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "(", ")"], lambda *x: x)
analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "(", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "PARAM_LIST"], lambda *x: x)

analizer.register_identifier("PARAM", ["EXPRESSION", ","], lambda *x: x)
analizer.register_identifier("PARAM", ["IDENTIFIER", ","], lambda *x: x)

analizer.register_identifier("PARAMS", ["(", "PARAM"], lambda *x: x)
analizer.register_identifier("PARAMS", ["PARAMS", "PARAM"], lambda *x: x)
analizer.register_identifier("PARAM_LIST", ["PARAMS", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("PARAM_LIST", ["PARAMS", "IDENTIFIER", ")"], lambda *x: x)

analizer.register_identifier("EXPRESSION", ["FUNC_CALL"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["STRING"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["FLOAT"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["A1"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["A1:A1"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["SHEET!A1"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["SHEET!A1:A1"], lambda *x: x)

analizer.register_identifier("EXPRESSION", ["EXPRESSION", "^", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "^", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "/", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "/", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "*", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "*", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "-", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "-", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "+", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "+", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "&", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "&", "EXPRESSION", ")"], lambda *x: x)

analizer.register_identifier("EXPRESSION", ["EXPRESSION", "=", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "=", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<>", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<>", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<=", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<=", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", ">=", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", ">=", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["EXPRESSION", ">", "EXPRESSION"], lambda *x: x)
analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", ">", "EXPRESSION", ")"], lambda *x: x)

analizer.register_identifier("FORMULA", ["=", "(", "EXPRESSION", ")"], lambda *x: x)
analizer.register_identifier("FORMULA", ["=", "EXPRESSION"], lambda *x: x)

