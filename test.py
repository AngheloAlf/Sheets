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


from typing import List, Tuple

from ASheets.parser import Token
from ASheets import utils



from ASheets.parser.representations.generic_expression import GenericExpression
from ASheets.parser.representations.data_types import TypeString, TypeNumber, TypeBoolean, TypeErrorGeneral, Constant
from ASheets.parser.representations.identifier import Identifier
from ASheets.parser.representations.a1 import A1, A1_A1, Sheet_A1
from ASheets.parser.representations.func_call import Param, Params, ParamList, FuncCall
from ASheets.parser.representations.binary_operator import BinaryOperator, Power, Divide, Multiply, Substract, Add, Concat, Equal, NotEqual, LessEqual, GreaterEqual, LessThan, GreaterThan
from ASheets.parser.representations.unary_operator import UnaryOperatorPre, UnaryOperatorPost, UnaryMinus, UnaryPlus, UnaryPercent
from ASheets.parser.representations.operation import Operation, OperationItem
from ASheets.parser.representations.reference import Reference, ReferenceItem, NamedRange
from ASheets.parser.representations.formula import Formula
from ASheets.parser.representations.abstract_representation import Start, ARepresentation


class TokenAnalizer():
    EMTPY = None

    def __init__(self):
        self._start = None
        self._starts = list()
        self._registered = list()

    def __str__(self):
        return "<TokenAnalizer>"
    def __repr__(self):
        return "<TokenAnalizer>"

    def register_start(self, identifier, sequence: List, callback=None):
        self._start = identifier
        self._starts.append(len(self._registered))
        self.register(identifier, sequence, callback)

    def register(self, identifier, sequence: List, callback=None):
        self._registered.append((identifier, (sequence, callback)))
        #if identifier not in self._registered:
        #    self._registered[identifier] = list()
        #self._registered[identifier].append((sequence, callback))


    def _is_nullable(self, rule, nullables):
        for x in rule[1][0]:
            if x not in nullables:
                return False
        return True

    def _update_nullables(self, nullables):
        for i in range(len(self._registered)):
            if self._is_nullable(self._registered[i], nullables):
                nullables.add(self._registered[i][0])

    def get_nullable_rules(self):
        nullables = set()
        old_size = -1
        while old_size != len(nullables):
            old_size = len(nullables)
            self._update_nullables(nullables)
        return nullables
    
    def _next_symbol(self, item):
        if item["next"] >= len(self._registered[item["rule"]]    [1][0]):
            return None
        return self._registered[item["rule"]]    [1][0]    [item["next"]]


    def _complete(self, S, i, j):
        item = S[i][j]
        for old_i in range(len(S[item["start"]])):
            old_item = S[item["start"]][old_i]
            if self._next_symbol(old_item) == item["name"]:
                aux = {"rule": old_item["rule"], "start": old_item["start"], "next": old_item["next"]+1, "name": old_item["name"]}
                append_no_repetition(S[i], aux)
                # S[i].append(aux)

    def _scan(self, S, i, j, symbol, tokens):
        item = S[i][j]
        if tokens[i] == symbol:
            if i + 1 >= len(S):
                S.append([])
            aux = {"rule": item["rule"], "start": item["start"], "next": item["next"]+1, "name": item["name"]}
            S[i+1].append(aux)

    def _predict(self, S, i, j, symbol, nullables):
        for rule_index in range(len(self._registered)):
            rule_name, rule = self._registered[rule_index]
            if rule_name == symbol:
                aux = {"rule": rule_index, "start": i, "next": 0, "name": rule_name}
                append_no_repetition(S[i], aux)
                # S[i].append(aux)
                if rule_name in nullables:
                    aux = {"rule": S[i][j]["rule"], "start": S[i][j]["start"], "next": S[i][j]["next"]+1, "name": S[i][j]["name"]}
                    append_no_repetition(S[i], aux)


    def _create_items(self, tokens: List[Token]):
        nullables = self.get_nullable_rules()
        S = [[]]
        for x in self._starts:
            S[0].append({"rule": x, "start": 0, "next": 0, "name": self._start})
        #print(len(tokens))
        #print()
        i = 0
        while i < len(S):
            #print(i)
            j = 0
            while j < len(S[i]):
                #print("\t", j, end="")
                symbol = self._next_symbol(S[i][j])
                if symbol == None:
                    #print(" complete")
                    self._complete(S, i, j)
                elif is_terminal(symbol):
                    #print(" scan")
                    self._scan(S, i, j, symbol, tokens)
                elif is_non_terminal(symbol):
                    #print(" predict")
                    self._predict(S, i, j, symbol, nullables)
                else:
                    print("Wat?")
                    exit(-1)
                j += 1
            i += 1
        
        return S
    
    def _invert_items(self, items):
        inverted = [[] for i in range(len(items))]
        for i in range(len(items)):
            # print(i)
            for y in items[i]:
                # print("\t", y, self._registered[y["rule"]][1][0])
                # print("\t", y, y["next"], len(self._registered[y["rule"]][1][0]))
                if y["next"] == len(self._registered[y["rule"]][1][0]):
                    y["end"] = i
                    inverted[y["start"]].append(y)
                    # print("\t", y, self._registered[y["rule"]][1][0])
            # print()
        return inverted

        """
    def _craete_tree(self, inverted_items, tokens, actual_name, i=0):
        # for i in range(len(inverted_items)):
        cosote = []
        for x in inverted_items[i]:
            if x["name"] == actual_name:
                #print(x, self._registered[x["rule"]][1][0])
                cosito = []
                k = 0
                for j in range(len(self._registered[x["rule"]][1][0])):
                    y = self._registered[x["rule"]][1][0][j]
                    if is_terminal(y):
                        print(i, j, len(cosito), y, tokens[i+j])
                        cosito.append(y)
                    elif is_non_terminal(y):
                        #print("\t", y)
                        sub_result = self._craete_tree(inverted_items, tokens, y, i=i+j)
                        if sub_result == None:
                            break
                        #print("\t\t", sub_result)
                        cosito.append(sub_result)
                        k += len(cosito)
                    else:
                        print("wat¿")
                        exit(-1)
                if len(cosito) == len(self._registered[x["rule"]][1][0]):
                    #print(cosito)
                    #print(len(cosito), len(self._registered[x["rule"]][1][0]))
                    #cosito = []
                    cosote.append(actual_name(self._registered[x["rule"]][1][0], cosito))
        #print()
        if len(cosote) == 0:
            return None
        if len(cosote) > 1:
            print("quedó la kagá")
            # print(cosote)
            for w in cosote:
                print("\t", w)
        return cosote
        """
    
        """
    def _tree_branch(self, inverted_items, tokens, item, rule_seq):
        branch = []
        start = item["start"]
        # end = start+1
        for x in rule_seq:
            if is_terminal(x):
                if start >= len(tokens):
                    print("start >= len(tokens)", start, len(tokens))
                    return None
                if tokens[start] != x:
                    print("tokens[start] != x", tokens[start], x)
                    return None
                print(tokens[start])
                branch.append(tokens[start])
                start += 1
            elif is_non_terminal(x):
                for y in inverted_items[start]:
                    if y["name"] == x:
                        print("\t", y)
                        # check(y)
                        algo = self._create_tree(inverted_items, tokens, y["name"], y["start"])
                        if algo == None:
                            # print("falló")
                            # exit(-1)
                            return None
                        branch.append(algo[0])
                        print("\nt!start", start, y["end"], algo[1], y)
                        if y["end"] - start != algo[1]:
                            return None
                        start = y["end"]
        """
                    
        """
        step = 0
        for x in rule_seq:
            print(x)
            if is_terminal(x):
                print(tokens[item["start"]+step], x)
                branch.append(x)
                step += 1
            elif is_non_terminal(x):
                aux = self._create_tree(inverted_items, tokens, x, item["start"]+step)
                if aux == None:
                    return None
                subtree, substep = aux
                step += substep
                branch.append(subtree)
        print("\t", len(branch), item["end"], step)
        if item["start"] + step != item["end"]:
            return None
        """
        """
        return branch
        """

        """
    def _create_tree(self, inverted_items, tokens, actual_name, i=0):
        cosita = []
        print("actual_name:", actual_name, " ~ ", "i:", i)
        for j in range(len(inverted_items[i])):
            x = inverted_items[i][j]
            if x["name"] == actual_name:
                rules = self._registered[x["rule"]][1][0]
                print(inverted_items[i][j], rules)
                branch = self._tree_branch(inverted_items, tokens, x, rules)
                if branch == None:
                    continue
                aux = actual_name(rules, branch)
                return (aux, len(branch))
                # print(aux)
                # cosita.append(aux)
                # exit(-1)
        return None
        # return cosita
        """

    def _get_produtions_matching_name_at(self, inverted_items, name, start):
        productions = []
        for item in inverted_items[start]:
            if item["name"] == name:
                productions.append(item)
        productions.sort(key=lambda x: x["end"]-x["start"], reverse=True)
        return productions

    def _test_subproduction(self, inverted_items, subtokens, sub_prod, substart):
        if sub_prod["end"] - sub_prod["start"] > len(subtokens):
            return None, -1
        return self._match_subtree(inverted_items, subtokens[substart:substart+sub_prod["end"]-sub_prod["start"]], sub_prod["name"], sub_prod["start"])


    def _match_subtree(self, inverted_items, subtokens, actual_name, start=0):
        items_with_actual_name = self._get_produtions_matching_name_at(inverted_items, actual_name, start)
        for item in items_with_actual_name:
            rules = self._registered[item["rule"]][1][0]
            substart = 0
            matchs = True
            data = []
            for rule in rules:
                if is_terminal(rule):
                    if subtokens[substart] == rule:
                        data.append(subtokens[substart])
                        substart += 1
                    else:
                        matchs = False
                        break
                else:
                    productions = self._get_produtions_matching_name_at(inverted_items, rule, start+substart)
                    matchs = False
                    for sub_prod in productions:
                        subdata, sub_substart = self._test_subproduction(inverted_items, subtokens, sub_prod, substart)
                        print(subdata)
                        if subdata is not None:
                            matchs = True
                            data.append(subdata)
                            substart += sub_substart
                            break
                    # substart += len(productions)
            if matchs:
                return (actual_name(rules, data), substart)
        return (None, -1)


    def parse(self, tokens: List[Token]):
        items = self._create_items(tokens)
        # print(len(items), len(tokens)+1)
        if len(items) != len(tokens)+1:
            return None
        inverted = self._invert_items(items)
        tree = self._match_subtree(inverted, tokens, self._start)
        print(tree)
        # tree = self._craete_tree(inverted, tokens, self._start)
        # print(len(tree))
        # print(tree[0])
        
        # print(self._craete_tree(inverted, tokens, self._start))
        """
        actual_name = self._start
        for i in range(len(inverted)):
            for x in inverted[i]:
                if x["name"] == actual_name:
                    pass
                print(x, self._registered[x["rule"]][1][0])
                for y in self._registered[x["rule"]][1][0]:
                    print(y)
                    if is_terminal(y):
                        pass
            print()
        """
        return inverted

    """
    def _match_subsequences(self, tokens, production):
        match_list = []
        #try:
        for subsequence, callback in self._registered[production]:
            sub_match, tokens_consumed_amount = self._parse(tokens, subsequence)
            #print(sub_match, tokens_consumed_amount)
            if sub_match is not None:
                match_list.append((production(subsequence, sub_match), tokens_consumed_amount))
                #print(production, sequence)
        #except RecursionError:
        #    print("puchita")
        #    print(production)
        #    print(tokens)
        #    exit(-1)
        return match_list

    def _parse(self, tokens: List[Token], test_sequence: List):
        #print(test_sequence)
        #print(tokens)
        index_token = 0
        index_sequence = 0
        # i = 0
        match = []
        while index_sequence < len(test_sequence):
            production = test_sequence[index_sequence]
            #print(production, end=" ")
            if is_terminal(production):
                #print(tokens[index_token], production == tokens[index_token])
                if production == tokens[index_token]:
                    match.append(tokens[index_token])
                    index_token += 1
                else:
                    return (None, -1)
            else:
                #print("\t is production")
                match_list = self._match_subsequences(tokens[index_token:], production)
                for sub_match, tokens_consumed_amount in match_list:
                    tail_match, j = self._parse(tokens[index_token+tokens_consumed_amount:], test_sequence[index_sequence+1:])
                    if tail_match is not None:
                        print(match)
                        print(sub_match)
                        print(tail_match)
                        print()
                        return (match + [sub_match] + tail_match, index_token + tokens_consumed_amount + j)
                return (None, -1)
            # i += 1
            index_sequence += 1
        return (match, index_token)

    def parse(self, tokens: List[Token]):
        for sequence, callback in self._start:
            print(self._parse(tokens, sequence))
        return "jue"
    """



    """
    def _parse(self, tokens: List[Token], test_sequence: List):
        #print(test_sequence)
        #print(tokens)
        i = 0
        match = []
        for production in test_sequence:
            #print(production, end=" ")
            if is_terminal(production):
                #print(tokens[i], production == tokens[i])
                if production == tokens[i]:
                    match.append(tokens[i])
                else:
                    return (None, -1)
            else:
                #print("\t is production")
                try:
                    did_match = False
                    for sequence, callback in self._registered[production]:
                        sub_match, j = self._parse(tokens[i:], sequence)
                        #print(sub_match, j)
                        if sub_match is not None:
                            match.append(production(sequence, sub_match))
                            #print(production, sequence)
                            i += j - 1
                            did_match = True
                            break
                    if not did_match:
                        return (None, -1)
                except RecursionError:
                    print("puchita")
                    print(i)
                    print(test_sequence)
                    print(production)
                    print(tokens[i:])
                    exit(-1)
            i += 1
        return (match, i)

    def parse(self, tokens: List[Token]):
        for sequence, callback in self._start:
            print(self._parse(tokens, sequence))
        return "jue"
    """

    """
    def _parse(self, tokens: List[Token]) -> List[Token]:
        tokens = list(tokens)
        for identf, data in self._registered.items():
            for pattern in data:
                sequence = pattern["sequence"]
                callback = pattern["callback"]
                i = 0
                while i < len(tokens):
                    if utils.match_at(sequence, tokens, i):
                        tokens_seq = utils.remove_range(tokens, i, len(sequence))
                        tokens.insert(i, Token(identf, callback(*tokens_seq)))
                        parsed = True
                    i += 1
        return tokens

    def parse(self, tokens: List[Token], iterout=5) -> Token:
        tokens = self._parse(tokens)
        last_len = len(tokens)
        equal_len = 0
        while len(tokens) > 1:
            tokens = self._parse(tokens)
            if len(tokens) == last_len:
                equal_len += 1
            else:
                equal_len = 0
            if equal_len > iterout:
                for x in tokens:
                    print(x)
                raise RuntimeError(f"iterout ({iterout}) exceeded.")
            last_len = len(tokens)
        return tokens[0]
    """

def is_terminal(prod):
    return isinstance(prod, str)

def is_non_terminal(prod):
    return issubclass(prod, ARepresentation)

def append_no_repetition(items_list, item):
    if item not in items_list:
        items_list.append(item)
"""
analizer = TokenAnalizer()

analizer.register_start(Start, ["=", Formula])
# analizer.register_start(Start, [Identifier, "(", ParamList, ")"])

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

analizer.register(TypeString, ["STRING"])
analizer.register(TypeNumber, ["NUMBER"])
analizer.register(TypeBoolean, ["BOOL"])
analizer.register(TypeErrorGeneral, ["ERROR_GENERAL"])


analizer.register(Reference, [ReferenceItem])
#analizer.register(Reference, [Prefix, Reference])
analizer.register(Reference, ["(", Reference, ")"])


analizer.register(ReferenceItem, [Sheet_A1])
analizer.register(ReferenceItem, [A1_A1])
analizer.register(ReferenceItem, [A1])
analizer.register(ReferenceItem, ["ERROR_REF"])
#analizer.register(ReferenceItem, [NamedRange])

analizer.register(Sheet_A1, ["SINGLE_QUOTE_STRING", "!", A1_A1])
analizer.register(Sheet_A1, ["SINGLE_QUOTE_STRING", "!", A1])
analizer.register(Sheet_A1, [Identifier, "!", A1_A1])
analizer.register(Sheet_A1, [Identifier, "!", A1])

analizer.register(A1_A1, [A1, ":", A1])
analizer.register(A1, ["CELL"])

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


analizer.register(Identifier, ["IDENTIFIER"])
"""



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

