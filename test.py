from __future__ import annotations
from ASheets.parser import parseFormula

from ASheets.parser.formula_parser import formulaTokenizer
from ASheets.parser.formula_parser import formulaAnalizer


def test_formula_tokenizer(formula: str, should_print=True):
    tokenized = formulaTokenizer.tokenize(formula)
    if should_print:
        for x in tokenized:
            print(x)
    return tokenized

def test_formula_analizer(formula: str, should_print=True):
    tokenized = formulaTokenizer.tokenize(formula)
    parsed = formulaAnalizer.parse(tokenized)
    if should_print:
        print(parsed)
    return parsed


def test_parseFormula(formula: str, should_print=True):
    parsed = parseFormula(formula)
    if should_print:
        print(parsed.token)
    return parsed


if __name__ == "__main__":
    formula1 = '=IF(OR($B102="", G$3=""), "", CALC_POINTS_FROM_RANGE(M102, M$4:M$203, someSheet!M$1:N$2, COLUMN(), someSheet!M$2) - ROW() + SUM(K$2:K4))'
    # print(formula1)
    formula2 = '=OR($B102="", ""=G$3)'
    print(formula2)
    tokens = test_formula_tokenizer(formula2, False)
    result = formulaAnalizer.parse(tokens)
    print(result)
    """
    for i in range(len(result)):
        print(i)
        for y in result[i]:
            print(y, "\t", analizer._registered[y["rule"]][1][0])
            pass
        print()
    """
    # test_formula_tokenizer(formula1)
