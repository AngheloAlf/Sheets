from __future__ import annotations
from typing import List, Tuple
from typing import Final, Union, Optional, NewType
# import json


class Token():
    def __init__(self, identifier: str, token: Union[str, List[Token]]):
        self.identifier: str = identifier
        self.token: Union[str, List[Token]] = token
    
    def stringify(self, deepness=0, indent=2):
        if isinstance(self.token, str):
            return (" "*indent*deepness) + f"{self.identifier}: {self.token}"
        result = (" "*indent*deepness) + f"{self.identifier}:\n"
        for i in self.token:
            result += i.stringify(deepness+1, indent) + "\n"
        result += (" "*indent*deepness) + f":{self.identifier}"
        return result

    def __str__(self):
        return self.stringify()
    
    def __repr__(self):
        return self.__str__()


TknMethod = NewType("TknMethod", str)

class Tokenizer():
    State_None: Final[str] = ""

    Method_Skip: Final[TknMethod] = TknMethod("SKP")
    Method_Sequence: Final[TknMethod] = TknMethod("SEQ")
    Method_Literal: Final[TknMethod] = TknMethod("LIT")
    Method_Cont_Char: Final[TknMethod] = TknMethod("CONT_CHAR")
    Method_Cont_Token: Final[TknMethod] = TknMethod("CONT_TKN")

    def __init__(self):
        self.registered: List[Tuple[TknMethod, Union[str, List[str], Tuple[str, str]], str]] = list()

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

    def register_token_container(self, left_char_container: str, right_char_container: str, identf: str):
        data = (Tokenizer.Method_Cont_Token, (left_char_container, right_char_container), identf)
        self.registered.append(data)


    def _tokenize(self, expression: str, end_char: str="") -> Tuple[int, List[Token]]:
        i = 0
        result: List[Token] = []
        state = Tokenizer.State_None
        token = ""
        while i < len(expression):
            char = expression[i]
            if char == end_char:
                break

            parsed = False
            for method, data, identf in self.registered:
                if method == Tokenizer.Method_Skip:
                    length = len(data)
                    literal = expression[i:i+length]
                    if literal == data:
                        if state != Tokenizer.State_None:
                            result.append(Token(state, token))
                            state = Tokenizer.State_None
                        parsed = True
                elif method == Tokenizer.Method_Sequence:
                    if char in data:
                        if state != identf:
                            if state != Tokenizer.State_None:
                                result.append(Token(state, token))
                            token = ""
                            state = identf
                        token += char
                        parsed = True
                elif method == Tokenizer.Method_Literal:
                    length = len(data)
                    literal = expression[i:i+length]
                    if literal == data:
                        if state != Tokenizer.State_None:
                            result.append(Token(state, token))
                        token = ""
                        state = Tokenizer.State_None
                        result.append(Token(identf, literal))
                        state = Tokenizer.State_None
                        parsed = True
                elif method == Tokenizer.Method_Cont_Char:
                    if char == data:
                        if state != Tokenizer.State_None:
                            result.append(Token(state, token))
                            state = Tokenizer.State_None
                        token = ""
                        i += 1
                        while expression[i] != data:
                            token += expression[i]
                            i += 1
                        result.append(Token(identf, token))
                        token = ""
                        parsed = True
                elif method == Tokenizer.Method_Cont_Token:
                    left, right = data
                    if char == left:
                        if state != Tokenizer.State_None:
                            result.append(Token(state, token))
                            state = Tokenizer.State_None
                        token = ""

                        j, sub_result = self._tokenize(expression[i+1:], right)
                        i += j + 1
                        result.append(Token(identf, sub_result))
                        parsed = True
                if parsed:
                    break
            
            if not parsed:
                print("Unknown char: " + char)

            i += 1
        if state != Tokenizer.State_None:
            result.append(Token(state, token))
        return i, result

    def tokenize(self, expression: str) -> Token:
        return Token("TOKEN", self._tokenize(expression)[1])


_special_symbols = ["$", ":", "!", "#", ",", "&"]
_arithmetic = ["+", "-", "*", "/", "=", "<", ">"]
_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
_normal_chars = ["_", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


formula_tokenizer = Tokenizer()
formula_tokenizer.register_skipable(" ", "SPACE")
formula_tokenizer.register_chars_container("'", "SINGLE_QUOTE_STRING")
formula_tokenizer.register_chars_container('"', "DOUBLE_QUOTE_STRING")
formula_tokenizer.register_token_container("(", ")", "PARENTHESES")
formula_tokenizer.register_token_container("{", "}", "CURLY")
formula_tokenizer.register_token_container("[", "]", "BRACKET")
formula_tokenizer.register_sequence(_special_symbols, "SYMBOL")
formula_tokenizer.register_sequence(_arithmetic, "SYMBOL")
formula_tokenizer.register_sequence(_numbers, "NUMBER")
formula_tokenizer.register_sequence(_normal_chars, "WORD")


if __name__ == "__main__":
    formula = '=IF(OR($B102="", G$3=""), "", CALC_POINTS_FROM_RANGE(M102, M$4:M$203, M$1, someSheet!M$2))'
    tokenized = formula_tokenizer.tokenize(formula[1:])
    print(tokenized)
    #print(json.dumps(tokenized, indent=2))
