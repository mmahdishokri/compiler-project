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


def read_token():
    global state
    l = len(tokens)
    while len(tokens) == l or tokens[-1][1] == 'WHITESPACE':
        state = get_next_token(state, word_wrapper, line_number_wrapper, tokens, errors)
    return tokens[-1]


def token_value(token):
    return token[2] if (token[1] in ['SYMBOL', 'KEYWORD']) else token[1]


def match_terminal(token, e):
    return token_value(token) == e


def match_rule(token, rule, A):
    for r in rule:
        if r in action_symbols:
            continue
        if r in terminals:
            return match_terminal(token, r)
        if token_value(token) in First[r]:
            return True
        if not EPS in First[r]:
            return False
    return token_value(token) in Follow[A]


def print_node(A, depth):
    for i in range(depth):
        print('\t', end='')
    print(A)

SS = []
PB = []
nxt_tmp = 0

def findaddr(inp):
    #TODO: look up the current input's address from Symbol Table
    return -1

def gettemp():
    global nxt_tmp
    res = nxt_tmp
    nxt_tmp += 1
    return res

def pid(inp):
    SS.append(findaddr(inp))

def subroutine(sym, inp=None):
    global it
    if sym == '#pid':
        pid(inp)
    if sym == '#assign':
        PB.append((':=', SS[-1], SS[-2]))
        SS.pop(2)
    if sym == '#add':
        t = gettemp()
        PB.append(('+', SS[-1], SS[-2], t))
        SS.pop(2)
        SS.append(t)



def parse_rule(rule, token_wrapper, depth):
    token = token_wrapper[0]
    expect_id = False
    for e in rule:
        if e in action_symbols:
            if e == '#pid':
                expect_id = True
            else:
                subroutine(e)
            continue
        if e in terminals:
            if match_terminal(token, e):
                if expect_id:
                    subroutine('#pid', token_value(token))
                print_node(token_value(token), depth + 1)
                token_wrapper[0] = token = read_token()
            else:
                if e == EOF:
                    errors.append((token[0], "Syntax error", 'Malfored Input'))
                    raise Exception('EOF Error')
                errors.append((token[0], "Syntax error", 'Missing ' + e))
        elif e in non_terminals:
            while token_value(token) not in First[e] and (token_value(token) not in Follow[e]):
                errors.append((token[0], "Syntax error", 'Unexpected ' + token[2]))
                token_wrapper[0] = token = read_token()
                if token[1] == 'EOF':
                    errors.append((token[0], "Syntax error", 'Unexpected EndOfFile'))
                    raise Exception('EOF Error')
            if token_value(token) not in First[e] and EPS not in First[e]:
                errors.append((token[0], "Syntax error", 'Missing ' + e))
            else:
                parse_non_terminal(e, token_wrapper, depth + 1)
            token = token_wrapper[0]
        else:
            print("PANIC")
            raise Exception("rule exception")
        expect_id = False


def parse_non_terminal(A, token_wrapper, depth=0):
    print_node(A, depth)
    token = token_wrapper[0]
    # TODO: CHECK THE NEXT CONDITION!!
    if EPS in First[A] and token_value(token) in Follow[A]:
        return
    for r in Rules[A]:
        if match_rule(token, r, A):
            parse_rule(r, token_wrapper, depth)
            return
    print("PANIC", A)
    raise Exception("non terminal exception")


print("Hello! I am your scanner ^_O")
code = open("All Tests/Parser/Test Error - 2", "r")
tokens = []
errors = []
state = 0
word_wrapper = [""]
line_number_wrapper = [1]

try:
    parse_non_terminal(START_NON_TERMINAL, [read_token()])
except:
    print('Parsing terminated due to an error.')

output_file = open("scanner.txt", "w")
error_file = open("errors.txt", "w")

print("Tokens:")
first_token_in_line = True
for my_token in tokens:
    # print(token[0], token[1])
    if not my_token[1] in ['WHITESPACE', 'COMMENT']:
        if first_token_in_line:
            output_file.write(str(my_token[0]) + ". ")
        first_token_in_line = False
        output_file.write('(' + my_token[1] + ', ' + my_token[2] + ') ')
    if my_token[2] == '\n':
        output_file.write("\n")
        first_token_in_line = True
output_file.close()

print("Errors:")
lastLine = -1
for error in errors:
    print('#' + str(error[0]) + ': ' + error[1] + '! ' + error[2])
    # if lastLine != error[0]:
    #    if lastLine != -1:
    #        error_file.write('\n')
    error_file.write('#' + str(error[0]) + ': ')
    error_file.write(error[1] + '! ' + error[2] + '\n')
    lastLine = error[0]
