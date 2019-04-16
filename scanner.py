import getchar
from constant import EOF_STATE, ACCEPT_STATE, START


def get_next_state(state, c):
    return state + 1


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

while state != EOF_STATE:
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

