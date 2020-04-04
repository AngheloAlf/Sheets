from typing import Tuple
import json

_state_none = 0
_special_symbols = ["$", ":", "!", "#", ","]
_state_symbols = 1
_arithmetic = ["+", "-", "*", "/", "=", "<", ">"]
_state_arithmetic = 2
_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
_state_numbers = 3
_normal_chars = _numbers + ["_", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
_state_normal_chars = 4

_state_single_quote_string = 5
_state_double_quote_string = 6

_state_parenthesis = 7
_state_curvy_brace = 8



def tokenize_formula(formula: str, end_char: str="") -> Tuple[int, list]:
    i = 0
    length = len(formula)
    result = []
    token = ""
    state = _state_none
    while i < length:
        char = formula[i]
        if char == " ": # skip spaces
            if state != _state_none:
                result.append((state, token))
                state = _state_none
        elif char == end_char:
            break
        elif char == "'":
            if state != _state_none:
                result.append((state, token))
            token = ""
            state = _state_none
            i += 1
            while formula[i] != "'":
                token += formula[i]
                i += 1
            result.append((_state_single_quote_string, token))
            token = ""
        elif char == '"':
            if state != _state_none:
                result.append((state, token))
            token = ""
            state = _state_none
            i += 1
            while formula[i] != '"':
                token += formula[i]
                i += 1
            result.append((_state_double_quote_string, token))
            token = ""
        elif char == "(":
            if state != _state_none:
                result.append((state, token))
            token = ""
            state = _state_none

            j, sub_result = tokenize_formula(formula[i+1:], ")")
            #j += 1
            i += j + 1
            result.append((_state_parenthesis, sub_result))

            #print(sub_result)
            #print(i, j, i+j, formula[i+j], formula)
            #exit(-1)
        elif char == "{":
            if state != _state_none:
                result.append((state, token))
            token = ""
            state = _state_none

            j, sub_result = tokenize_formula(formula[i+1:], "}")
            i += j + 1
            result.append((_state_curvy_brace, sub_result))
        else:
            if char in _special_symbols:
                if state != _state_none:
                    result.append((state, token))
                token = ""
                state = _state_none
                result.append((_state_symbols, char))
            elif char in _arithmetic:
                if state != _state_arithmetic:
                    if state != _state_none:
                        result.append((state, token))
                    token = ""
                    state = _state_arithmetic
                token += char
            elif char in _numbers and state != _state_normal_chars:
                if state != _state_numbers:
                    if state != _state_none:
                        result.append((state, token))
                    token = ""
                    state = _state_numbers
                token += char
            elif char in _normal_chars:
                if state != _state_normal_chars:
                    if state != _state_none:
                        result.append((state, token))
                    token = ""
                    state = _state_normal_chars
                token += char
        i += 1
    if state != _state_none:
        result.append((state, token))
    return i, result


def tokenize_constant(expression: str):
    return NotImplemented


def tokenize(expression: str):
    if len(expression) == 0:
        return None
    if expression[0] == "=":
        return tokenize_formula(expression[1:])[1]
    return tokenize_constant(expression)


if __name__ == "__main__":
    formula = '=IF(OR($B102="", G$3=""), "", CALC_POINTS_FROM_RANGE(M102, M$4:M$203, M$1, someSheet!M$2))'
    tokenized = tokenize(formula)
    print(tokenized)
    #print(json.dumps(tokenized, indent=2))
