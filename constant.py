ACCEPT_STATE = 1
START = 0
EOF = 1
SYM = 2
SYM2 = 3
SYM3 = 4
CMT = 5
CMT2 = 6
CMT3 = 7
CMT4 = 8
CMT5 = 9
CMT6 = 10
WHS = 11
NUM = 12
ID = 13
ACCEPT_STATES = [EOF, SYM, SYM2, SYM3, CMT5, CMT6, WHS, NUM, ID]
STATE_TYPE = {
    EOF: 'EOF',
    SYM: 'SYMBOL',
    SYM2: 'SYMBOL',
    SYM3: 'SYMBOL',
    CMT5: 'COMMENT',
    CMT6: 'COMMENT',
    WHS: 'WHITESPACE',
    NUM: 'NUM',
    ID: 'ID',
}
KEYWORDS = ['if', 'else', 'void', 'int', 'while', 'break', 'continue', 'switch', 'default', 'case', 'return',]
EPS = 'eps'
START_NON_TERMINAL = 'program'

Rules = {}
f = open('ll1-2.txt', 'r')
for line in f:
    lhs, rhs = map(str.strip, line.split('->'))
    Rules.setdefault(lhs, []).append(rhs.split(' '))
non_terminals = list(Rules.keys())
terminals = []
action_symbols = []
for rules in Rules.values():
    for rule in rules:
        for r in rule:
            if not r in non_terminals:
                if r[0] != '#' and not r in terminals:
                    terminals.append(r)
                elif r[0] == '#' and not r in action_symbols:
                    action_symbols.append(r)

print(non_terminals)
print(terminals)
print(action_symbols)

First = {}
for t in terminals:
    First[t] = [t]
fin = False
while not fin:
    fin = True
    for X in non_terminals:
        for rule in Rules[X]:
            f = True
            for r in rule:
                if not EPS in First.setdefault(r, []):
                    for a in First[r]:
                        if not a in First.setdefault(X, []):
                            First.setdefault(X, []).append(a)
                            fin = False
                    f = False
                    break
            if f and not EPS in First.setdefault(X, []):
                First.setdefault(X, []).append(EPS)
                fin = False

Follow = {START_NON_TERMINAL : ['EOF']}
fin = False
while not fin:
    fin = True
    for A in non_terminals:
        for rule in Rules[A]:
            f = True
            first = []
            for X in reversed(rule):
                if X in non_terminals:
                    if f:
                        for a in Follow[A]:
                            if not a in Follow.setdefault(X, []):
                                Follow.setdefault(X, []).append(a)
                                fin = False
                    for a in first:
                        if a != EPS and not a in Follow.setdefault(X, []):
                            Follow.setdefault(X, []).append(a)
                            fin = False
                if EPS in First[X]:
                    first.extend(First[X])
                else:
                    first = First[X].copy()
                    f = False
