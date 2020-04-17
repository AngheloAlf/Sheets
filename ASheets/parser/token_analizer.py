from __future__ import annotations
from typing import List, Tuple
from typing import Type, Optional

from .token import Token
from .representations.abstract_representation import ARepresentation
from .. import utils


class RuleSequence():
    def __init__(self, name: Type[ARepresentation], sequence: List, callback):
        self._name = name
        self._sequence = sequence
        self._callback = callback


class EarleyItem():
    def __init__(self, ruleId: Optional[int]=None, name: Optional[Type[ARepresentation]]=None, nextPos: int=0, start: int=0, end=None, *, item: Optional[EarleyItem]=None):
        if item is not None:
            self._ruleId: int = item.ruleId
            self._name: Type[ARepresentation] = item.name
            self._nextPos: int = item.nextPos
            self._start: int = item.start
            self._end: int = item.end
        else:
            if ruleId is None or name is None:
                raise ValueError("Invalid parameters.")
            self._ruleId = ruleId
            self._name = name
            self._nextPos = nextPos
            self._start = start
            self._end = end

    @property
    def ruleId(self) -> int:
        return self._ruleId
    @property
    def name(self) -> Type[ARepresentation]:
        return self._name
    @property
    def nextPos(self) -> int:
        return self._nextPos
    @property
    def start(self) -> int:
        return self._start
    @property
    def end(self) -> int:
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

    def advance(self):
        self._nextPos += 1


class EarleyStateSet():
    def __init__(self, setId: int):
        self._items: List[EarleyItem] = []
        self._setId: int = setId

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        return self._items[key]
    
    def newItem(self, ruleId: int, name: Type[ARepresentation], *, unique: bool=False):
        item = EarleyItem(ruleId, name, start=self._setId)
        if unique and item in self._items:
            return
        self._items.append(item)
        return

    def addItemNext(self, item: EarleyItem, *, unique: bool=False):
        nextItem = EarleyItem(item=item)
        nextItem.advance()
        if unique and nextItem in self._items:
            return
        self._items.append(nextItem)
        return

    def addItem(self, item: EarleyItem):
        self._items.append(item)
        return


class EarleyParser():
    def __init__(self, rules, startName: Type[ARepresentation], startsIndexes: List[int]):
        self._rules = rules
        self._S: List[EarleyStateSet] = [EarleyStateSet(0)]
        for rule_index in startsIndexes:
            self._S[0].newItem(rule_index, startName)


    def _is_nullable(self, rule, nullables: set) -> bool:
        for x in rule[1]:
            if x not in nullables:
                return False
        return True

    def _update_nullables(self, nullables):
        for i in range(len(self._rules)):
            if self._is_nullable(self._rules[i], nullables):
                nullables.add(self._rules[i][0])
        return

    def get_nullable_rules(self):
        nullables = set()
        old_size = -1
        while old_size != len(nullables):
            old_size = len(nullables)
            self._update_nullables(nullables)
        return nullables


    def _next_symbol(self, item: EarleyItem):
        sequence = self._rules[item.ruleId][1]
        if item.nextPos >= len(sequence):
            return None
        return sequence[item.nextPos]


    def _complete(self, i: int, actual_item: EarleyItem):
        start_set_of_item = self._S[actual_item.start]
        for old_i in range(len(start_set_of_item)):
            old_item = start_set_of_item[old_i]
            if self._next_symbol(old_item) == actual_item.name:
                self._S[i].addItemNext(old_item, unique=True)
        return

    def _scan(self, i: int, symbol, tokens: List, actual_item: EarleyItem):
        if tokens[i] == symbol:
            if i + 1 >= len(self._S):
                self._S.append(EarleyStateSet(i+1))
            self._S[i+1].addItemNext(actual_item)
        return

    def _predict(self, i: int, symbol: Type[ARepresentation], actual_item: EarleyItem, nullables):
        for rule_index in range(len(self._rules)):
            rule_name, rule, callback = self._rules[rule_index]
            if rule_name == symbol:
                self._S[i].newItem(rule_index, rule_name, unique=True)
                if rule_name in nullables:
                    self._S[i].addItemNext(actual_item, unique=True)
        return


    def _invert_items(self) -> List[EarleyStateSet]:
        inverted: List[EarleyStateSet] = [EarleyStateSet(i) for i in range(len(self._S))]
        for i in range(len(self._S)):
            for y in self._S[i]:
                if y.nextPos == len(self._rules[y.ruleId][1]):
                    y._end = i
                    inverted[y.start].addItem(y)
        return inverted


    def parse(self, tokens):
        nullables = self.get_nullable_rules()
        i = 0
        while i < len(self._S):
            state_set = self._S[i]
            j = 0
            while j < len(state_set):
                actual_item = state_set[j]
                symbol = self._next_symbol(actual_item)
                if symbol == None:
                    self._complete(i, actual_item)
                elif is_terminal(symbol):
                    self._scan(i, symbol, tokens, actual_item)
                elif is_non_terminal(symbol):
                    self._predict(i, symbol, actual_item, nullables)
                else:
                    print("Wat?")
                    exit(-1)
                j += 1
            i += 1
        inverted = self._invert_items()
        return inverted


class TokenAnalizer():
    def __init__(self):
        self._start: Optional[Type[ARepresentation]] = None
        self._starts: List[int] = list()
        self._registered = list()

    def __str__(self):
        return "<TokenAnalizer>"
    def __repr__(self):
        return "<TokenAnalizer>"

    def register_start(self, identifier: Type[ARepresentation], sequence: List, callback=None):
        self._start = identifier
        self._starts.append(len(self._registered))
        self.register(identifier, sequence, callback)

    def register(self, identifier, sequence: List, callback=None):
        self._registered.append((identifier, sequence, callback))


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
                        if subdata is not None:
                            matchs = True
                            data.append(subdata)
                            substart += sub_substart
                            break
            if matchs:
                return (actual_name(rules, data), substart)
        return (None, -1)


    def parse(self, tokens: List[Token]):
        if self._start is None:
            raise RuntimeError("Start point has not been setted.")
        parser = EarleyParser(self._registered, self._start, self._starts)
        items = parser.parse(tokens)
        if len(items) != len(tokens)+1:
            return None
        tree = self._match_subtree(items, tokens, self._start)
        return tree[0]


def is_terminal(prod):
    return isinstance(prod, str)

def is_non_terminal(prod):
    return issubclass(prod, ARepresentation)
