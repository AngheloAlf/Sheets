from __future__ import annotations
from typing import List, Tuple, Dict, Callable
from typing import Final, Union, Optional, NewType, cast
import re

from .token import Token
from .. import utils


TknMethod_t = NewType("TknMethod_t", str)

class Tokenizer():
    Method_Skip: Final[TknMethod_t] = TknMethod_t("SKIP")
    Method_Store: Final[TknMethod_t] = TknMethod_t("STORE")

    def __init__(self):
        self._registered: List[Tuple[str, str]] = list()
        self._name_data: Dict[str, Tuple[TknMethod_t, Callable[[Token], Token]]] = dict()
        self._reg_expr: Optional[re.Pattern] = None
        self._compiled: bool = False

    def register_skipable(self, name: str, reg_expression: str, callback: Callable[[Token], Token]=lambda x: x):
        self._registered.append((name, reg_expression))
        self._name_data[name] = (Tokenizer.Method_Skip, callback)
        self._compiled = False

    def register(self, name: str, reg_expression: str, callback: Callable[[Token], Token]=lambda x: x):
        self._registered.append((name, reg_expression))
        self._name_data[name] = (Tokenizer.Method_Store, callback)
        self._compiled = False


    def tokenize(self, formula: str) -> List[Token]:
        if not self._compiled or self._reg_expr is None:
            expr = '|'.join(f"(?P<{name}>{expression})" for name, expression in self._registered)
            self._reg_expr = re.compile(expr)
            self._compiled = True

        result = []
        for match in self._reg_expr.finditer(formula):
            name: str = cast(str, match.lastgroup)
            value: str = match.group()
            method, callback = self._name_data[name]
            if method == Tokenizer.Method_Store:
                result.append(callback(Token(name, value)))
        return result
