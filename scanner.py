import getchar
from constant import *


def isblank(c):
    return ord(c) == 32 or ord(c) == 10 or ord(c) == 13 or ord(c) == 9 or ord(c) == 11 or ord(c) == 12


def isnum(c):
    return ord('9') >= ord(c) >= ord('0')


def issymb(c):
    return c == '=' or c == ';' or c == ':' or c == ',' or c == '[' or c == ']' or c == '(' or c == ')' or c == '{' or c == '}' or c == '+' or c == '-' or c == '*' or c == '<'


def iseof(c):
    return False


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

    if state == NUM:
        if isnum(c):
            return NUM

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


def get_state_type(state):
    return ACCEPT_STATE


def get_next_token(state, word_wrapper, tokens, errors):
    word = word_wrapper[0]
    c = code.read(1)
    print("c = ", c)
    next_state = get_next_state(state, c)
    if next_state == -1:
        if get_state_type(state) == ACCEPT_STATE:
            next_state = get_next_state(START, c)
            if next_state != -1:
                tokens.append((get_state_type(state), word))
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

    return next_state


print("Hello! I am your scanner ^_^")

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

print("Errors:")
for error in errors:
    print(error[0], error[1])

