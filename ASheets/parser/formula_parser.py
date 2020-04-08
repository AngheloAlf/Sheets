from __future__ import annotations
from typing import List, Tuple
from typing import Final, Union, Optional, NewType
import re

from .token import Token
from .tokenizer import Tokenizer
from .token_analizer import TokenAnalizer
from .. import utils

from .representations.generic_expression import GenericExpression
from .representations.data_types import TypeString, TypeFloat
from .representations.identifier import Identifier
from .representations.a1 import A1, A1_A1, Sheet_A1
from .representations.func_call import Param, Params, ParamList, FuncCall
from .representations.binary_arithmetic import Power, Divide, Multiply, Substract, Add, Concat
from .representations.comparison import Equal, NotEqual, LessEqual, GreaterEqual, LessThan, GreaterThan
from .representations.formula import Formula


def configureFormulaTokenizer(tokenizer: Tokenizer) -> None:
    tokenizer.register_skipable("SPACE", r"\s+")

    tokenizer.register("IDENTIFIER", r"[a-zA-Z_]([a-zA-Z_0-9])*")
    tokenizer.register("NUMBER", r"(\d+(\.\d+)?)|(\.(\d+))")

    brackets = [
        ("L_PAREN", "("), 
        ("R_PAREN", ")"), 
        ("L_CURLY", "{"), 
        ("R_CURLY", "}"), 
        ("L_BRACKET", "["), 
        ("R_BRACKET", "]")
    ]
    symbols = [
        ("DOLLAR", "$"), 
        ("COLON", ":"), 
        ("EXCLAM", "!"), 
        ("NUMB_SIGN", "#"), 
        ("DOT", "."), 
        ("COMMA", ","), 
        ("SEMI_COLON", ";"), 
        ("QUOT", "'"), 
        ("QUOT_DOUBLE", "\"")
    ]
    binary_arithmetic_ops = [
        ("ADD", "+"), 
        ("SUB", "-"), 
        ("MULT", "*"), 
        ("DIV", "/"), 
        ("EXPONENT", "^"), 
        ("AMPERSAND", "&")
    ]
    unary_arithmetic_ops = [
        ("PERCENT", "%"), 
    ]
    equality_ops = [
        ("EQUAL", "="), 
        ("NOTEQUAL", "<>"), 
        ("LQ", "<="), 
        ("GQ", ">="), 
        ("LT", "<"), 
        ("GT", ">")
    ]
    for name, expression in brackets+symbols+binary_arithmetic_ops+unary_arithmetic_ops+equality_ops:
        tokenizer.register(name, re.escape(expression), lambda x: Token(x.token, x.token))

    def error_callback(x):
        raise ValueError(f"Unrecognized value: {x}")
    tokenizer.register("ERROR", r".", lambda x: error_callback)
    return


def configureFormulaAnalizer(analizer: TokenAnalizer) -> None:
    analizer.register_identifier("A1", ["WORD", "$", "NUMBER"], lambda *x: A1(x[0], x[2], fixed_row=True))
    analizer.register_identifier("A1", ["$", "WORD", "NUMBER"], lambda *x: A1(x[1], x[2], fixed_col=True))
    analizer.register_identifier("A1", ["$", "WORD", "$", "NUMBER"], lambda *x: A1(x[1], x[3], fixed_col=True, fixed_row=True))

    analizer.register_identifier("STRING", ["SINGLE_QUOTE_STRING"], lambda *x: TypeString(x[0]))
    analizer.register_identifier("STRING", ["DOUBLE_QUOTE_STRING"], lambda *x: TypeString(x[0]))

    analizer.register_identifier("FLOAT", ["NUMBER", ".", "NUMBER"], lambda *x: TypeFloat(x[0], x[2]))

    analizer.register_identifier("IDENTIFIER", ["WORD", "NUMBER"], lambda *x: Identifier(x[0], x[1]))
    analizer.register_identifier("IDENTIFIER", ["WORD"], lambda *x: Identifier(x[0]))
    analizer.register_identifier("IDENTIFIER", ["IDENTIFIER", "WORD"], lambda *x: Identifier(x[0], x[1]))
    analizer.register_identifier("IDENTIFIER", ["IDENTIFIER", "NUMBER"], lambda *x: Identifier(x[0], x[1]))

    analizer.register_identifier("A1:A1", ["A1", ":", "A1"], lambda *x: A1_A1(x[0], x[2]))
    analizer.register_identifier("A1:A1", ["A1", ":", "IDENTIFIER"], lambda *x: A1_A1(x[0], x[2]))
    analizer.register_identifier("A1:A1", ["IDENTIFIER", ":", "A1"], lambda *x: A1_A1(x[0], x[2]))

    analizer.register_identifier("SHEET!A1", ["IDENTIFIER", "!", "A1"], lambda *x: Sheet_A1(x[0], x[2]))
    analizer.register_identifier("SHEET!A1:A1", ["IDENTIFIER", "!", "A1:A1"], lambda *x: Sheet_A1(x[0], x[2]))

    analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "(", ")"], lambda *x: FuncCall(x[0]))
    analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "(", "EXPRESSION", ")"], lambda *x: FuncCall(x[0], param=x[2]))
    analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "(", "IDENTIFIER", ")"], lambda *x: FuncCall(x[0], param=x[2]))
    analizer.register_identifier("FUNC_CALL", ["IDENTIFIER", "PARAM_LIST"], lambda *x: FuncCall(x[0], param_list=x[1]))

    analizer.register_identifier("PARAM", ["EXPRESSION", ","], lambda *x: Param(x[0]))
    analizer.register_identifier("PARAM", ["IDENTIFIER", ","], lambda *x: Param(x[0]))
    analizer.register_identifier("PARAMS", ["(", "PARAM"], lambda *x: Params(x[1]))
    analizer.register_identifier("PARAMS", ["PARAMS", "PARAM"], lambda *x: Params(x[1], x[0]))
    analizer.register_identifier("PARAM_LIST", ["PARAMS", "EXPRESSION", ")"], lambda *x: ParamList(x[0], x[1]))
    analizer.register_identifier("PARAM_LIST", ["PARAMS", "IDENTIFIER", ")"], lambda *x: ParamList(x[0], x[1]))

    analizer.register_identifier("EXPRESSION", ["FUNC_CALL"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["STRING"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["FLOAT"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["A1"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["A1:A1"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["SHEET!A1"], lambda *x: GenericExpression(x[0]))
    analizer.register_identifier("EXPRESSION", ["SHEET!A1:A1"], lambda *x: GenericExpression(x[0]))

    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "^", "EXPRESSION"], lambda *x: Power(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "^", "EXPRESSION", ")"], lambda *x: Power(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "/", "EXPRESSION"], lambda *x: Divide(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "/", "EXPRESSION", ")"], lambda *x: Divide(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "*", "EXPRESSION"], lambda *x: Multiply(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "*", "EXPRESSION", ")"], lambda *x: Multiply(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "-", "EXPRESSION"], lambda *x: Substract(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "-", "EXPRESSION", ")"], lambda *x: Substract(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "+", "EXPRESSION"], lambda *x: Add(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "+", "EXPRESSION", ")"], lambda *x: Add(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "&", "EXPRESSION"], lambda *x: Concat(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "&", "EXPRESSION", ")"], lambda *x: Concat(x[1], x[3]))

    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "=", "EXPRESSION"], lambda *x: Equal(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "=", "EXPRESSION", ")"], lambda *x: Equal(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<>", "EXPRESSION"], lambda *x: NotEqual(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<>", "EXPRESSION", ")"], lambda *x: NotEqual(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<=", "EXPRESSION"], lambda *x: LessEqual(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<=", "EXPRESSION", ")"], lambda *x: LessEqual(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", ">=", "EXPRESSION"], lambda *x: GreaterEqual(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", ">=", "EXPRESSION", ")"], lambda *x: GreaterEqual(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", "<", "EXPRESSION"], lambda *x: LessThan(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", "<", "EXPRESSION", ")"], lambda *x: LessThan(x[1], x[3]))
    analizer.register_identifier("EXPRESSION", ["EXPRESSION", ">", "EXPRESSION"], lambda *x: GreaterThan(x[0], x[2]))
    analizer.register_identifier("EXPRESSION", ["(", "EXPRESSION", ">", "EXPRESSION", ")"], lambda *x: GreaterThan(x[1], x[3]))

    analizer.register_identifier("FORMULA", ["=", "(", "EXPRESSION", ")"], lambda *x: Formula(x[2]))
    analizer.register_identifier("FORMULA", ["=", "EXPRESSION"], lambda *x: Formula(x[1]))

    return


formulaTokenizer = Tokenizer()
formulaAnalizer = TokenAnalizer()

configureFormulaTokenizer(formulaTokenizer)
configureFormulaAnalizer(formulaAnalizer)


def parseFormula(formula: str) -> Token:
    return formulaAnalizer.parse(formulaTokenizer.tokenize(formula))

