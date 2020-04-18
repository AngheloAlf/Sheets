from __future__ import annotations
from typing import List, Tuple
from typing import Final, Union, Optional, NewType
import re

from .token import Token
from .tokenizer import Tokenizer
from .token_analizer import TokenAnalizer
from .. import utils

from .representations.terminals import *

from .representations.generic_expression import GenericExpression
from .representations.data_types import TypeString, TypeNumber, TypeBoolean, TypeErrorGeneral, Constant
from .representations.identifier import Identifier
from .representations.a1 import A1, A1_A1, Sheet_A1
from .representations.func_call import Param, Params, ParamList, FuncCall
from .representations.binary_operator import BinaryOperator, Power, Divide, Multiply, Substract, Add, Concat, Equal, NotEqual, LessEqual, GreaterEqual, LessThan, GreaterThan
from .representations.unary_operator import UnaryOperatorPre, UnaryOperatorPost, UnaryMinus, UnaryPlus, UnaryPercent
from .representations.operation import Operation, OperationItem
from .representations.reference import Reference, ReferenceItem, NamedRange
from .representations.formula import Formula
from .representations.abstract_representation import Start, ARepresentation


def configureFormulaTokenizer(tokenizer: Tokenizer) -> None:
    tokenizer.register_skipable(SPACE, r"\s+")

    tokenizer.register(BOOL, r"TRUE|FALSE")

    tokenizer.register(CELL, r"\$?[A-Z]+\$?[1-9]([0-9]*)")

    tokenizer.register(ERROR_REF, r"\#REF!")
    tokenizer.register(ERROR_GENERAL, r"(\#NULL!)|(\#DIV/0)|(\#VALUE!)|(\#NAME?)|(\#NUM!)|(\#N/A)")

    tokenizer.register(STRING, r'"([^"]*)"')
    tokenizer.register(SINGLE_QUOTE_STRING, r"([^']*)'")
    tokenizer.register(IDENTIFIER, r"[a-zA-Z_]([a-zA-Z_0-9])*")
    tokenizer.register(NUMBER, r"(\d+(\.\d+)?)|(\.(\d+))")

    brackets = [
        (L_PAREN, "("), 
        (R_PAREN, ")"), 
        (L_CURLY, "{"), 
        (R_CURLY, "}"), 
        (L_BRACKET, "["), 
        (R_BRACKET, "]")
    ]
    symbols = [
        (DOLLAR, "$"), 
        (COLON, ":"), 
        (EXCLAM, "!"), 
        (NUMB_SIGN, "#"), 
        (DOT, "."), 
        (COMMA, ","), 
        (SEMI_COLON, ";"), 
        (QUOT, "'"), 
        (QUOT_DOUBLE, "\"")
    ]
    binary_arithmetic_ops = [
        (ADD, "+"), 
        (SUB, "-"), 
        (MULT, "*"), 
        (DIV, "/"), 
        (EXPONENT, "^"), 
        (AMPERSAND, "&")
    ]
    unary_arithmetic_ops = [
        (PERCENT, "%"), 
    ]
    equality_ops = [
        (EQUAL, "="), 
        (NOTEQUAL, "<>"), 
        (LQ, "<="), 
        (GQ, ">="), 
        (LT, "<"), 
        (GT, ">")
    ]
    for name, expression in brackets+symbols+binary_arithmetic_ops+unary_arithmetic_ops+equality_ops:
        tokenizer.register(name, re.escape(expression))

    def error_callback(x):
        raise ValueError(f"Unrecognized value: {x}")
    tokenizer.register(Terminal("__ERROR"), r".", error_callback)
    return


def configureFormulaAnalizer(analizer: TokenAnalizer) -> None:
    analizer.register_start(Start, ["=", Formula])

    analizer.register(Formula, [Constant])
    analizer.register(Formula, [FuncCall])
    analizer.register(Formula, [Reference])
    #analizer.register(Formula, [Operation])
    # analizer.register(Formula, [ConstantArray])
    analizer.register(Formula, ["(", Formula, ")"])

    analizer.register(Constant, [TypeString])
    analizer.register(Constant, [TypeNumber])
    analizer.register(Constant, [TypeBoolean])
    analizer.register(Constant, [TypeErrorGeneral])

    analizer.register(TypeString, [STRING])
    analizer.register(TypeNumber, [NUMBER])
    analizer.register(TypeBoolean, [BOOL])
    analizer.register(TypeErrorGeneral, [ERROR_GENERAL])


    analizer.register(Reference, [ReferenceItem])
    #analizer.register(Reference, [Prefix, Reference])
    analizer.register(Reference, ["(", Reference, ")"])


    analizer.register(ReferenceItem, [Sheet_A1])
    analizer.register(ReferenceItem, [A1_A1])
    analizer.register(ReferenceItem, [A1])
    analizer.register(ReferenceItem, [ERROR_REF])
    #analizer.register(ReferenceItem, [NamedRange])

    analizer.register(Sheet_A1, [SINGLE_QUOTE_STRING, "!", A1_A1])
    analizer.register(Sheet_A1, [SINGLE_QUOTE_STRING, "!", A1])
    analizer.register(Sheet_A1, [Identifier, "!", A1_A1])
    analizer.register(Sheet_A1, [Identifier, "!", A1])

    analizer.register(A1_A1, [A1, ":", A1])
    analizer.register(A1, [CELL])

    analizer.register(NamedRange, [Identifier])


    analizer.register(FuncCall, [Identifier, "(", ")"])
    # analizer.register(FuncCall, [Identifier, "(", Param, ")"])
    analizer.register(FuncCall, [Identifier, "(", ParamList, ")"])

    # analizer.register(Param, [Formula, ","])
    # analizer.register(Params, ["(", Param])
    # analizer.register(Params, [Params, Param])
    # analizer.register(ParamList, [Params, Formula, ")"])

    analizer.register(Param, [Constant])
    analizer.register(Param, [FuncCall])
    analizer.register(Param, [Operation])
    analizer.register(Param, [Reference])
    # analizer.register(Param, [ConstantArray])
    analizer.register(Param, ["(", Param, ")"])

    #analizer.register(Params, [Param])
    #analizer.register(Params, [Params, ",", Param])
    analizer.register(ParamList, [Param, ",", ParamList])
    analizer.register(ParamList, [Param])


    # analizer.register(Operation, [Formula, BinaryOperator, Formula])
    # analizer.register(Operation, [UnaryOperatorPre, Formula])
    # analizer.register(Operation, [Formula, UnaryOperatorPost])
    analizer.register(Operation, [OperationItem, BinaryOperator, OperationItem])
    analizer.register(Operation, [UnaryOperatorPre, OperationItem])
    analizer.register(Operation, [OperationItem, UnaryOperatorPost])


    analizer.register(OperationItem, [Constant])
    analizer.register(OperationItem, [FuncCall])
    analizer.register(OperationItem, [Reference])
    # analizer.register(OperationItem, [Operation])
    # analizer.register(OperationItem, [ConstantArray])
    analizer.register(OperationItem, ["(", OperationItem, ")"])


    # TODO: fix operator precedence
    analizer.register(BinaryOperator, [Power])
    analizer.register(BinaryOperator, [Divide])
    analizer.register(BinaryOperator, [Multiply])
    analizer.register(BinaryOperator, [Substract])
    analizer.register(BinaryOperator, [Add])
    analizer.register(BinaryOperator, [Concat])
    analizer.register(BinaryOperator, [Equal])
    analizer.register(BinaryOperator, [NotEqual])
    analizer.register(BinaryOperator, [LessEqual])
    analizer.register(BinaryOperator, [GreaterEqual])
    analizer.register(BinaryOperator, [LessThan])
    analizer.register(BinaryOperator, [GreaterThan])

    analizer.register(Power, ["^"])
    analizer.register(Divide, ["/"])
    analizer.register(Multiply, ["*"])
    analizer.register(Substract, ["-"])
    analizer.register(Add, ["+"])
    analizer.register(Concat, ["&"])
    analizer.register(Equal, ["="])
    analizer.register(NotEqual, ["<>"])
    analizer.register(LessEqual, ["<="])
    analizer.register(GreaterEqual, [">="])
    analizer.register(LessThan, ["<"])
    analizer.register(GreaterThan, [">"])

    analizer.register(UnaryOperatorPre, [UnaryPlus])
    analizer.register(UnaryOperatorPre, [UnaryMinus])
    analizer.register(UnaryOperatorPost, [UnaryPercent])

    analizer.register(UnaryPlus, ["+"])
    analizer.register(UnaryMinus, ["-"])
    analizer.register(UnaryPercent, ["%"])

    analizer.register(Identifier, [IDENTIFIER])

    return


formulaTokenizer = Tokenizer()
formulaAnalizer = TokenAnalizer()

configureFormulaTokenizer(formulaTokenizer)
configureFormulaAnalizer(formulaAnalizer)

def parseFormula(formula: str):
    return formulaAnalizer.parse(formulaTokenizer.tokenize(formula))
