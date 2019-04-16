import getchar
from constant import *


def isblank(c):
    return ord(c) == 32 or ord(c) == 10 or ord(c) == 13 or ord(c) == 9 or ord(c) == 11 or ord(c) == 12


def isnum(c):
    return ord('9') >= ord(c) >= ord('0')


def issymb(c):
    return c == '=' or c == ';' or c == ':' or c == ',' or c == '[' or c == ']' or c == '(' or c == ')' or c == '{' or c == '}' or c == '+' or c == '-' or c == '*' or c == '<'


def isalpha(c):
    return (ord('a') <= ord(c) <= ord('z')) or (ord('A') <= ord(c) <= ord('Z'))


def iseof(c):
    return c == ''


def get_next_state(state, c):
    if state == START:
        if iseof(c):
            return EOF
        if isblank(c):
            return WHS
        if isnum(c):
            return NUM
        if c == '/':
            return CMT
        if c == '=':
            return SYM2
        if issymb(c):
            return SYM
        if isalpha(c):
            return ID

    if state == NUM:
        if isnum(c):
            return NUM

    if state == ID:
        if isnum(c) or isalpha(c):
            return ID

    if state == CMT:
        if c == '*':
            return CMT2
        if c == '/':
            return CMT3

    if state == CMT2:
        if c == '*':
            return CMT4
        return CMT2

    if state == CMT3:
        if ord(c) == 10:
            return CMT5
        return CMT3

    if state == CMT4:
        if c == '/':
            return CMT6
        if c == '*':
            return CMT4
        return CMT2

    if state == SYM2:
        if c == '=':
            return SYM3

    return -1


def is_accept(state):
    return state in ACCEPT_STATES


def get_type(state, word):
    if STATE_TYPE[state] == 'ID' and word in KEYWORDS:
        return 'KEYWORD'
    return STATE_TYPE[state]


def get_next_token(state, word_wrapper, tokens, errors):
    word = word_wrapper[0]
    c = code.read(1)
    next_state = get_next_state(state, c)
    print("c = ", c, end="")
    print(", next_state = ", next_state)
    if next_state == -1:
        if is_accept(state):
            next_state = get_next_state(START, c)
            if next_state != -1:
                tokens.append((get_type(state, word), word))
                word = ""
                word += c
            else:
                errors.append((word + c, "invalid input"))
                word = ""
                next_state = START
        else:
            errors.append((word + c, "invalid input"))
            word = ""
            next_state = START
    else:
        word += c
    word_wrapper[0] = word
    return next_state


print("Hello! I am your scanner ^_O")

code = open("code.c", "r")
output_file = open("scanner.txt", "w")
error_file = open("lexical_errors.txt", "w")

tokens = []
errors = []
state = 0
wrapper = [""]

while state != EOF:
    state = get_next_token(state, wrapper, tokens, errors)
    print("state = ", state)
    print("word = ", wrapper[0])
    print("tokens =", tokens)
    print("errors = ", errors)

print("Tokens:")
for token in tokens:
    print(token[0], token[1])
    if not token[0] in ['WHITESPACE', 'COMMENT',]:
        output_file.write('(' + token[0] + ', ' + token[1] + ') ')
    if token[1] == '\n':
        output_file.write("\n")
output_file.close()


print("Errors:")
for error in errors:
    print(error[0], error[1])
    error_file