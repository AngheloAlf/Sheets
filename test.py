from ASheets.parser import tokenizer
from ASheets.parser import token_analizer


if __name__ == "__main__":
    formula = '=IF(OR($B102="", G$3=""), "", CALC_POINTS_FROM_RANGE(M102, M$4:M$203, someSheet!M$1:N$2, COLUMN(), someSheet!M$2) - ROW() + SUM(K$2:K4))'
    tokenized = tokenizer.formula_tokenizer.tokenize(formula)
    # for x in tokenized:
    #     print(x)
    parsed = token_analizer.analizer.parse(tokenized)
    print(formula)
    print(parsed.token)
