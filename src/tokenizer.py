from typing import List, Tuple
import json

class Tokenizer():
    State_None = None
    Type_Skip = "SKP"
    Type_Sequence = "SEQ"
    Type_Literal = "LIT"
    Type_Cont_Char = "CONT_CHAR"
    Type_Cont_Token = "CONT_TKN"

    def __init__(self):
        self.registered = list()

    def register_skipable(self, literal: str, identf: str, options=None):
        data = (Tokenizer.Type_Skip, literal, identf)
        self.registered.append(data)

    def register_sequence(self, character_list: List[str], identf: str, options=None):
        data = (Tokenizer.Type_Sequence, character_list, identf)
        self.registered.append(data)

    def register_literal(self, literal: str, identf: str, options=None):
        data = (Tokenizer.Type_Literal, literal, identf)
        self.registered.append(data)

    def register_chars_container(self, char_container: str, identf: str, options=None):
        data = (Tokenizer.Type_Cont_Char, char_container, identf)
        self.registered.append(data)

    def register_token_container(self, left_char_container: str, right_char_container: str, identf: str, options=None):
        data = (Tokenizer.Type_Cont_Token, (left_char_container, right_char_container), identf)
        self.registered.append(data)


    def _tokenize(self, expression: str, end_char: str=""):
        i = 0
        result = []
        state = Tokenizer.State_None
        token = ""
        while i < len(expression):
            char = expression[i]
            if char == end_char:
                break

            parsed = False
            for type_, data, identf in self.registered:
                if type_ == Tokenizer.Type_Skip:
                    length = len(data)
                    if expression[i:i+length] == data:
                        if state != Tokenizer.State_None:
                            result.append((state, token))
                            state = Tokenizer.State_None
                        parsed = True
                elif type_ == Tokenizer.Type_Sequence:
                    if char in data:
                        if state != identf:
                            if state != Tokenizer.State_None:
                                result.append((state, token))
                            token = ""
                            state = identf
                        token += char
                        parsed = True
                elif type_ == Tokenizer.Type_Literal:
                    pass # TODO
                elif type_ == Tokenizer.Type_Cont_Char:
                    if char == data:
                        if state != Tokenizer.State_None:
                            result.append((state, token))
                            state = Tokenizer.State_None
                        token = ""
                        i += 1
                        while expression[i] != data:
                            token += expression[i]
                            i += 1
                        result.append((identf, token))
                        token = ""

                        parsed = True
                elif type_ == Tokenizer.Type_Cont_Token:
                    left, right = data
                    if char == left:
                        if state != Tokenizer.State_None:
                            result.append((state, token))
                            state = Tokenizer.State_None
                        token = ""

                        j, sub_result = self._tokenize(expression[i+1:], right)
                        i += j + 1
                        result.append((identf, sub_result))
                        parsed = True
                if parsed:
                    break
            
            if not parsed:
                print("Unknown char: " + char)

            i += 1
        if state != Tokenizer.State_None:
            result.append((state, token))
        return i, result

    def tokenize(self, expression: str):
        return self._tokenize(expression)[1]


_special_symbols = ["$", ":", "!", "#", ",", "&"]
_arithmetic = ["+", "-", "*", "/", "=", "<", ">"]
_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
_normal_chars = _numbers + ["_", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


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
