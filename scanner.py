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


def get_next_token(state, word_wrapper, line_number_wrapper, tokens, errors):
    word = word_wrapper[0]
    c = code.read(1)
    next_state = get_next_state(state, c)
    # print("c = ", c, end="")
    # print(", next_state = ", next_state)
    line_number = line_number_wrapper[0]
    if next_state == -1:
        if is_accept(state):
            next_state = get_next_state(START, c)
            if next_state != -1:
                tokens.append((line_number, get_type(state, word), word))
                word = ""
                word += c
            else:
                errors.append((line_number, "Invalid input", word + c))
                word = ""
                next_state = START
        else:
            errors.append((line_number, "Invalid input", word + c))
            word = ""
            next_state = START
    else:
        word += c
    word_wrapper[0] = word
    if c == '\n':
        line_number_wrapper[0] += 1
    return next_state


print("Hello! I am your scanner ^_O")
code = open("code.c", "r")
tokens = []
errors = []
state = 0
word_wrapper = [""]
line_number_wrapper = [1]

def read_token():
    global state
    l = len(tokens)
    while len(tokens) == l:
        state = get_next_token(state, word_wrapper, line_number_wrapper, tokens, errors)
    return tokens[-1]

def match_terminal(token, e):
    return token[2] == e if token[1] == 'SYMBOL' else token[1] == e

def match_rule(token, rule):
    for r in rule:
        if r in terminals:
            return match_terminal(token, r)
        if token in First[r]:
            return True
        if not EPS in First[r]:
            return False
    return False

def parse_rule(rule, token):
    for e in rule:
        if e in terminals:
            if match_terminal(token, e):
                token = read_token()
            else:
                errors.append((token[0], "Syntax error", 'Missing ' + e))
        elif e in non_terminals:
            while not token in First[e] and not token in Follow[e]:
                errors.append((token[0], "Syntax error", 'Unexpected ' + token[2]))
                token = read_token()
            if not token in First[e] and not EPS in First[e]:
                errors.append((token[0], "Syntax error", 'Missing ' + e))
            parse_non_terminal(e)
        else:
            print("PANIC")
            raise Exception("rule exception")

def parse_non_terminal(A, token):
    if EPS in First[A] and token in Follow[A]:
        return
    for r in Rules[A]:
        if match_rule(token, r):
            parse_rule(r, token)
            return
    print("PANIC")
    raise Exception("non terminal exception")


# stack = [start[S]]
# while len(stack) > 0:
#     fin = False
#     cur = stack[-1]
#     if is_finish[cur]:
#         stack.pop()
#         continue
#     for term in go[cur]:
#         if token == term:
#             fin = True
#             stack[-1] = go[cur][term]
#             state = get_next_token(state, word_wrapper, line_number_wrapper, tokens, errors)
#             token = tokens[-1]
#             break
#     if fin:
#         continue
#     for non_term in Go[cur]:
#         if token in First[non_term] or (EPS in First[non_term] and token in Follow[non_term]):
#             fin = True
#             #stack[-1] = Go[cur][non_term]
#             stack.append(start[non_term])
#     if fin:
#         continue
#     if EPS in Go[cur] and token in Follow[owner[cur]]:
#         stack[-1] = go[cur][EPS]
#         fin = True
#     if not fin:
#         print("Error")
#


# while state != EOF:
#     read_token()
#     print("state = ", state)
#     print("word = ", word_wrapper[0])
#     print("tokens =", tokens)
#     print("errors = ", errors)

parse_non_terminal('program', read_token())

output_file = open("scanner.txt", "w")
error_file = open("errors.txt", "w")

print("Tokens:")
first_token_in_line = True
for token in tokens:
    print(token[0], token[1])
    if not token[1] in ['WHITESPACE', 'COMMENT']:
        if first_token_in_line:
            output_file.write(str(token[0]) + ". ")
        first_token_in_line = False
        output_file.write('(' + token[1] + ', ' + token[2] + ') ')
    if token[2] == '\n':
        output_file.write("\n")
        first_token_in_line = True
output_file.close()


print("Errors:")
lastLine = -1
for error in errors:
    print(error[1], error[2])
    if lastLine != error[0]:
        if lastLine != -1:
            error_file.write('\n')
        error_file.write('#' + str(error[0]) + ': ')
    error_file.write(error[1] + '! ' + error[2])
    lastLine = error[0]

