from __future__ import annotations
from typing import List, Tuple
from typing import Optional

from .token import Token
from .representations.abstract_representation import ARepresentation
from .. import utils


class EarleyItem():
    def __init__(self, ruleId=None, name=None, nextPos=None, start=None, end=None, *, item: Optional[EarleyItem]=None):
        if item is not None:
            self._ruleId = item.ruleId
            self._name = item.name
            self._nextPos = item.nextPos
            self._start = item.start
            self._end = item.end
        else:
            if ruleId is None or name is None or nextPos is None or start is None:
                raise ValueError("Invalid parameters.")
            self._ruleId = ruleId
            self._name = name
            self._nextPos = nextPos
            self._start = start
            self._end = end

    @property
    def ruleId(self):
        return self._ruleId
    @property
    def name(self):
        return self._name
    @property
    def nextPos(self):
        return self._nextPos
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._end

    def __eq__(self, other):
        if self.ruleId != other.ruleId:
            return False
        if self.name != other.name:
            return False
        if self.nextPos != other.nextPos:
            return False
        if self.start != other.start:
            return False
        if self.end != other.end:
            return False
        return True


class TokenAnalizer():
    def __init__(self):
        self._start = None
        self._starts: List[int] = list()
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
        self._registered.append((identifier, sequence, callback))


    def _is_nullable(self, rule, nullables):
        for x in rule[1]:
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
        if item.nextPos >= len(self._registered[item.ruleId][1]):
            return None
        return self._registered[item.ruleId][1][item.nextPos]


    def _complete(self, S, i, j):
        item = S[i][j]
        for old_i in range(len(S[item.start])):
            old_item = S[item.start][old_i]
            if self._next_symbol(old_item) == item.name:
                aux = EarleyItem(old_item.ruleId, old_item.name, old_item.nextPos+1, old_item.start)
                append_no_repetition(S[i], aux)

    def _scan(self, S, i, j, symbol, tokens):
        item = S[i][j]
        if tokens[i] == symbol:
            if i + 1 >= len(S):
                S.append([])
            aux = EarleyItem(item.ruleId, item.name, item.nextPos+1, item.start)
            S[i+1].append(aux)

    def _predict(self, S, i, j, symbol, nullables):
        for rule_index in range(len(self._registered)):
            rule_name, rule, callback = self._registered[rule_index]
            if rule_name == symbol:
                aux = EarleyItem(rule_index, rule_name, 0, i)
                append_no_repetition(S[i], aux)
                if rule_name in nullables:
                    aux = EarleyItem(S[i][j].ruleId, S[i][j].name, S[i][j].nextPos+1, S[i][j].start)
                    append_no_repetition(S[i], aux)


    def _create_items(self, tokens: List[Token]):
        nullables = self.get_nullable_rules()
        S = [[]]
        for x in self._starts:
            S[0].append(EarleyItem(x, self._start, 0, 0))
        #print(len(tokens))
        #print()
        i = 0
        while i < len(S):
            # print(i)
            j = 0
            while j < len(S[i]):
                # print("\t", j)
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
                if y.nextPos == len(self._registered[y.ruleId][1]):
                    y._end = i
                    inverted[y.start].append(y)
                    # print("\t", y, self._registered[y["rule"]][1][0])
            # print()
        return inverted


    def _get_produtions_matching_name_at(self, inverted_items, name, start):
        productions = []
        for item in inverted_items[start]:
            if item.name == name:
                productions.append(item)
        productions.sort(key=lambda x: x.end-x.start, reverse=True)
        return productions

    def _test_subproduction(self, inverted_items, subtokens, sub_prod, substart):
        if sub_prod.end - sub_prod.start > len(subtokens):
            return None, -1
        return self._match_subtree(inverted_items, subtokens[substart:substart+sub_prod.end-sub_prod.start], sub_prod.name, sub_prod.start)


    def _match_subtree(self, inverted_items, subtokens, actual_name, start=0):
        items_with_actual_name = self._get_produtions_matching_name_at(inverted_items, actual_name, start)
        for item in items_with_actual_name:
            rules = self._registered[item.ruleId][1]
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
                        # print(subdata)
                        if subdata is not None:
                            matchs = True
                            data.append(subdata)
                            substart += sub_substart
                            break
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
        # print(tree)
        return tree[0]


def is_terminal(prod):
    return isinstance(prod, str)

def is_non_terminal(prod):
    return issubclass(prod, ARepresentation)

def append_no_repetition(items_list, item):
    if item not in items_list:
        items_list.append(item)
    return
