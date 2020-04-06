from ASheets.parser import parseFormula

from ASheets.parser.formula_parser import formulaTokenizer
from ASheets.parser.formula_parser import formulaAnalizer


def test_formula_tokenizer(formula: str):
    tokenized = formulaTokenizer.tokenize(formula)
    for x in tokenized:
        print(x)
    return

def test_formula_analizer(formula: str):
    tokenized = formulaTokenizer.tokenize(formula)
    parsed = formulaAnalizer.parse(tokenized)
    print(parsed)


def test_parseFormula(formula: str):
    parsed = parseFormula(formula)
    print(parsed.token)



if __name__ == "__main__":
    formula1 = '=IF(OR($B102="", G$3=""), "", CALC_POINTS_FROM_RANGE(M102, M$4:M$203, someSheet!M$1:N$2, COLUMN(), someSheet!M$2) - ROW() + SUM(K$2:K4))'
    print(formula1)
    test_formula_tokenizer(formula1)

