from __future__ import annotations

from ..terminal import Terminal


SPACE = Terminal("SPACE")

BOOL = Terminal("BOOL")

CELL = Terminal("CELL")

ERROR_REF = Terminal("ERROR_REF")
ERROR_GENERAL = Terminal("ERROR_GENERAL")

STRING = Terminal("STRING")
SINGLE_QUOTE_STRING = Terminal("SINGLE_QUOTE_STRING")
IDENTIFIER = Terminal("IDENTIFIER")
NUMBER = Terminal("NUMBER")

L_PAREN = Terminal("(", "L_PAREN")
R_PAREN = Terminal(")", "R_PAREN")
L_CURLY = Terminal("{", "L_CURLY")
R_CURLY = Terminal("}", "R_CURLY")
L_BRACKET = Terminal("[", "L_BRACKET")
R_BRACKET = Terminal("]", "R_BRACKET")

DOLLAR = Terminal("$", "DOLLAR")
COLON = Terminal(":", "COLON")
EXCLAM = Terminal("!", "EXCLAM")
NUMB_SIGN = Terminal("#", "NUMB_SIGN")
DOT = Terminal(".", "DOT")
COMMA = Terminal(",", "COMMA")
SEMI_COLON = Terminal(";", "SEMI_COLON")
QUOT = Terminal("'", "QUOT")
QUOT_DOUBLE = Terminal("\"", "QUOT_DOUBLE")

ADD = Terminal("+", "ADD")
SUB = Terminal("-", "SUB")
MULT = Terminal("*", "MULT")
DIV = Terminal("/", "DIV")
EXPONENT = Terminal("^", "EXPONENT")
AMPERSAND = Terminal("&", "AMPERSAND")

PERCENT = Terminal("%", "PERCENT")

EQUAL = Terminal("=", "EQUAL")
NOTEQUAL = Terminal("<>", "NOTEQUAL")
LQ = Terminal("<=", "LQ")
GQ = Terminal(">=", "GQ")
LT = Terminal("<", "LT")
GT = Terminal(">", "GT")
