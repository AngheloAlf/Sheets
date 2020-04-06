from __future__ import annotations
from typing import List, Tuple
from typing import Final, Union, Optional, NewType

from .token import Token
from .. import utils


TknMethod = NewType("TknMethod", str)

class Tokenizer():
    State_None: Final[str] = ""

    Method_Skip: Final[TknMethod] = TknMethod("SKP")
    Method_Sequence: Final[TknMethod] = TknMethod("SEQ")
    Method_Literal: Final[TknMethod] = TknMethod("LIT")
    Method_Cont_Char: Final[TknMethod] = TknMethod("CONT_CHAR")
    Method_Cont_Token: Final[TknMethod] = TknMethod("CONT_TKN")

    def __init__(self):
        self.registered: List[Tuple[TknMethod, Union[str, List[str], Tuple[str, str]], Union[str, Tuple[str, str]]]] = list()

    def register_skipable(self, literal: str, identf: str):
        data = (Tokenizer.Method_Skip, literal, identf)
        self.registered.append(data)

    def register_sequence(self, character_list: List[str], identf: str):
        data = (Tokenizer.Method_Sequence, character_list, identf)
        self.registered.append(data)

    def register_literal(self, literal: str, identf: str):
        data = (Tokenizer.Method_Literal, literal, identf)
        self.registered.append(data)

    def register_chars_container(self, char_container: str, identf: str):
        data = (Tokenizer.Method_Cont_Char, char_container, identf)
        self.registered.append(data)

    def register_token_container(self, left_char_container: str, right_char_container: str, left_identf: str, right_identf):
        data = (Tokenizer.Method_Cont_Token, (left_char_container, right_char_container), (left_identf, right_identf))
        self.registered.append(data)


    def _tokenize(self, expression: str, end_char: str="") -> Tuple[int, List[Token]]:
        i = 0
        result: List[Token] = []
        state = Tokenizer.State_None
        token = ""
        def _state_change():
            nonlocal state
            nonlocal token
            if state != Tokenizer.State_None:
                result.append(Token(state, token))
                state = Tokenizer.State_None
                token = ""

        while i < len(expression):
            char = expression[i]
            if char == end_char:
                break

            parsed = False
            for method, data, identf in self.registered:
                if method == Tokenizer.Method_Skip:
                    if utils.match_at(data, expression, i):
                        _state_change()
                        parsed = True
                elif method == Tokenizer.Method_Sequence:
                    if char in data:
                        if state != identf:
                            _state_change()
                            state = identf
                        token += char
                        parsed = True
                elif method == Tokenizer.Method_Literal:
                    if utils.match_at(data, expression, i):
                        _state_change()
                        result.append(Token(identf, data))
                        parsed = True
                elif method == Tokenizer.Method_Cont_Char:
                    if char == data:
                        _state_change()
                        i += 1
                        container = ""
                        while expression[i] != data:
                            container += expression[i]
                            i += 1
                        result.append(Token(identf, container))
                        parsed = True
                elif method == Tokenizer.Method_Cont_Token:
                    left, right = data
                    if char == left:
                        _state_change()
                        left_identf, right_identf = identf
                        result.append(Token(left_identf, char))
                        i += 1
                        j, sub_result = self._tokenize(expression[i:], right)
                        i += j
                        result += sub_result
                        result.append(Token(right_identf, expression[i]))
                        #result.append(Token(identf, sub_result))
                        parsed = True
                if parsed:
                    break
            
            if not parsed:
                print("Unknown char: " + char)

            i += 1
        if state != Tokenizer.State_None:
            result.append(Token(state, token))
        return i, result

    def tokenize(self, expression: str) -> List[Token]:
        return self._tokenize(expression)[1]
