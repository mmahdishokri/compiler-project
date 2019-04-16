import getchar
from constant import *

def isblank(c):
    return ord(c) == 32 or ord(c) == 10 or ord(c) == 13 or ord(c) == 9 or ord(c) == 11 or ord(c) == 12


def isnum(c):
    return ord('9') >= ord(c) >= ord('0')


def issymb(c):
    return c == '=' or c == ';' or c == ':' or c == ',' or c == '[' or c == ']' or c == '(' or c == ')' or c == '{' or c == '}' or c == '+' or c == '-' or c == '*' or c == '<'


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


def get_next_token(state, word_wrapper, tokens):
    word = word_wrapper[0]
    c = code.read(1)
    word = word + c
    next_state = get_next_state(state, c)
    tokens.append(word)
    return next_state


print("Hello! I am your scanner ^_^")

c = input()
print(ord(c))

# code = open("code.c", "r")
# output = open("scanner.txt")
# errors = open("lexical_errors.txt")
#
# tokens = []
# state = 0
# word_wrapper = [""]
#
# while state != EOF:
#     state = get_next_token(state, word_wrapper, tokens)