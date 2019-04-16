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