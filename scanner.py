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
        if r in terminals and r != EPS:
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


class STObject:
    def __init__(self, type, address):
        self.type = type
        self.address = address

    def __str__(self):
        return self.type, self.address


class SSObject:
    def __init__(self, type, value, indirect=False):
        self.type = type
        self.value = value
        self.indirect = indirect

    def __str__(self):
        return self.type, self.value, self.indirect


ST = {}                 # symbol table
FT = {}                 # function table
SS = []                 # semantic stack
PB = []                 # program block
PS = []                 # parse stack
TS = []                 # type stack
SC = []                 # scope stack
nxt_tmp = 1000
nxt_addr = 0
sizeof = {
    'int': 4,
    'void': 0,
}


def allocate_address(size):
    global nxt_addr
    res = nxt_addr
    nxt_addr += size
    return res


def declare_int(inp, len):
    address = allocate_address(sizeof['int']*len)
    ST[inp] = STObject('int', address)


def findaddr(inp):
    if inp not in ST:
        raise Exception('Variable ' + str(inp) + ' not defined.')
    return ST[inp].address


def gettemp():
    global nxt_tmp
    res = nxt_tmp
    nxt_tmp += sizeof['int']
    return res


def pid(inp, def_type = ''):
    pid_type = 'hoy'
    if def_type != '':
        pid_type = def_type
    else:
        for i in range(len(PS)):
            x = PS[-i - 1]
            if x in ['dec-list', 'params', 'exp']:
                pid_type = x
                break
    print('pid!! type = ', pid_type)
    if pid_type == 'dec-list':
        SS.append(SSObject((TS[-1], 'id-name'), inp))
    if pid_type == 'params':
        if TS[-1] == 'void':
            raise Exception('Illegal type of void. For variable: ' + str(inp))
        SS.append(SSObject((TS[-1], 'param-name'), inp))
    if pid_type == 'exp':
        if inp not in FT:
            SS.append(SSObject('var-addr', findaddr(inp)))
        else:
            SS.append(SSObject('fun-addr', findaddr(inp)))


def get_val(x):
    if x.type == 'cons':
        return '#' + str(x.value)
    if x.indirect:
        return '@' + str(x.value)
    return x.value


def check_int(x):
    if x.type not in ['exp-addr', 'cons', 'var-addr']:
        raise Exception('Type mismatch in operands.')


def print_ss():
    for s in SS:
        print('(' + str(s.type), str(s.value), str(s.indirect)+')', end=', ')
    print()


def subroutine(sym, inp=None):
    print('subroutine!! o|^_^|o ', sym)
    print_ss()

    if sym == '#pid':
        pid(inp)

    if sym == '#assign':
        val = SS[-2]
        PB.append(('ASSIGN', get_val(SS[-1]), get_val(val)))
        SS.pop()
        SS.pop()
        SS.append(SSObject('exp-addr', val.value, val.indirect))

    if sym == '#add':
        t = gettemp()
        check_int(SS[-1])
        check_int(SS[-2])
        PB.append(('ADD', get_val(SS[-1]), get_val(SS[-2]), t))
        SS.pop()
        SS.pop()
        SS.append(SSObject('exp-addr', t))

    if sym == '#sub':
        t = gettemp()
        check_int(SS[-1])
        check_int(SS[-2])
        PB.append(('SUB', get_val(SS[-1]), get_val(SS[-2]), t))
        SS.pop()
        SS.pop()
        SS.append(SSObject('exp-addr', t))

    if sym == '#negate':
        SS.append(SSObject('flag', 'negate'))

    if sym == '#do-negate':
        check_int(SS[-1])
        if SS[-1].type == 'cons':
            t = gettemp()
            PB.append(('SUB', '#0', get_val(SS[-1]), t))
            SS.pop()
            SS.append(SSObject('exp-addr', t))
        else:
            PB.append(('SUB', '#0', get_val(SS[-1]), get_val(SS[-1])))
        assert SS[-2].value == 'negate'
        SS.pop(-2)

    if sym == '#save-num':
        SS.append(SSObject('cons', inp))

    if sym == '#save-one':
        SS.append(SSObject('cons', 1))

    if sym == '#var-dec':
        if TS[-1] == 'void':
            raise Exception('Illegal type of void. For variable: ' + str(SS[-2].value))
        declare_int(SS[-2].value, SS[-1].value)
        SS.pop()
        SS.pop()

    if sym == '#pop':
        SS.pop()

    if sym == '#mult':
        t = gettemp()
        check_int(SS[-1])
        check_int(SS[-2])
        PB.append(('MULT', get_val(SS[-1]), get_val(SS[-2]), t))
        SS.pop()
        SS.pop()
        SS.append(SSObject('exp-addr', t))

    if sym == '#fun-dec-start':
        SS.append(SSObject('flag', 'params-start'))

    if sym == '#fun-dec-end':
        params = []
        while SS[-1].value != 'params-start':
            params.append(SS[-1])
            SS.pop()
        SS.pop()
        FT[SS[-1].value] = (type, params)

    if sym == '#arr-ref':
        check_int(SS[-1])
        t = gettemp()
        PB.append(('MULT', get_val(SS[-1]), '#4', t))
        PB.append(('ADD', '#'+str(SS[-2].value), t, t))
        SS.pop()
        SS.pop()
        SS.append(SSObject('exp-addr', t, True))

    if sym == '#save-pb':
        SS.append(SSObject('cons', len(PB)))
        PB.append(())

    if sym == '#jpf-save':
        PB[SS[-1].value] = ('JPF', get_val(SS[-2]), len(PB) + 1)
        SS.pop()
        SS.pop()
        SS.append(SSObject('cons', len(PB)))
        PB.append(())

    if sym == '#jp':
        PB[SS[-1].value] = ('JP', len(PB))

    if sym == '#label':
        SS.append(SSObject('cons', len(PB)))

    if sym == '#while':
        PB[SS[-1].value] = (('JPF', get_val(SS[-2]), len(PB) + 1))
        PB.append(('JP', SS[-3].value))
        SS.pop()
        SS.pop()
        SS.pop()


def parse_rule(rule, token_wrapper, depth):
    token = token_wrapper[0]
    expect_id = False
    expect_num = False
    for e in rule:
        if e in action_symbols:
            expect_num = expect_id = False
            if e == '#pid':
                expect_id = True
            elif e == '#save-num':
                expect_num = True
            else:
                try:
                    subroutine(e)
                except Exception as exception:
                    errors.append((token[0], "Semantic error", str(exception)))
                    raise exception
            continue
        if e in terminals and e != EPS:
            if match_terminal(token, e):
                if token_value(token) == 'ID':
                    if expect_id:
                        try:
                            subroutine('#pid', token[2])
                        except Exception as exception:
                            errors.append((token[0], "Semantic error", str(exception)))
                            raise exception
                    # SS.append(token[2])                WHY??
                if token_value(token) == 'NUM':
                    if expect_num:
                        subroutine('#save-num', int(token[2]))
                print_node(token_value(token), depth + 1)
                PS.append(token_value(token))
                if token[2] in ['int', 'void']:
                    TS.append(token[2])
                token_wrapper[0] = token = read_token()
            else:
                if e == EOF:
                    errors.append((token[0], "Syntax error", 'Malformed Input'))
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
        elif e != EPS:
            print("PANIC")
            raise Exception("rule exception")
        expect_id = False
        expect_num = False


def parse_non_terminal(A, token_wrapper, depth=0):
    print_node(A, depth)
    PS.append(A)
    token = token_wrapper[0]
    # TODO: CHECK THE NEXT CONDITION!!
    # if EPS in First[A] and token_value(token) in Follow[A]:
    #   return
    for r in Rules[A]:
        if match_rule(token, r, A):
            parse_rule(r, token_wrapper, depth)
            while PS[-1] != A:
                PS.pop()
            PS.pop()
            return
    print("PANIC", A)
    raise Exception("non terminal exception")


print("\nHello! I am your scanner, parser, semantic analyser, and intermediate code generator! ^_O\n")

print("Here is your parse tree:")

code = open("All Tests/Parser/My_Test.txt", "r")
tokens = []
errors = []
state = 0
word_wrapper = [""]
line_number_wrapper = [1]

try:
    parse_non_terminal(START_NON_TERMINAL, [read_token()])
except Exception as e:
    print('Parsing terminated due to an error:', e)

parser_output_file = open("scanner.txt", "w")
error_file = open("errors.txt", "w")
output_file = open("output.txt", "w")

print("Tokens:")
first_token_in_line = True
for my_token in tokens:
    # print(token[0], token[1])
    if not my_token[1] in ['WHITESPACE', 'COMMENT']:
        if first_token_in_line:
            parser_output_file.write(str(my_token[0]) + ". ")
        first_token_in_line = False
        parser_output_file.write('(' + my_token[1] + ', ' + my_token[2] + ') ')
    if my_token[2] == '\n':
        parser_output_file.write("\n")
        first_token_in_line = True
parser_output_file.close()

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


PB.append(('PRINT', 0))
PB.append(('PRINT', 4))
PB.append(('PRINT', 8))
PB.append(('PRINT', 12))

print("Program Block:")
print(PB)

command_number = 0
for command in PB:
    command = list(command)
    command.extend(['']*(4 - len(command)))
    output_file.write(str(command_number) + '\t(' + str(command[0]))
    output_file.write(', ' + str(command[1]))
    output_file.write(', ' + str(command[2]))
    output_file.write(', ' + str(command[3]) + ')\n')
    command_number = command_number + 1
