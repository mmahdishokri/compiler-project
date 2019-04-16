import getchar
from constant import EOF_STATE

def get_next_state(state, c):
    return state + 1

def get_next_token(state, word_wrapper, tokens):
    word = word_wrapper[0]
    c = code.read(1)
    word = word + c
    next_state = get_next_state(state, c)
    tokens.append(("type", word))
    return next_state

print("Hello! I am your scanner ^_^")

code = open("code.c", "r")
output = open("scanner.txt", "w")
errors = open("lexical_errors.txt", "w")

tokens = []
state = 0
word_wrapper = [""]

while state != EOF_STATE:
    state = get_next_token(state, word_wrapper, tokens)

for token in tokens:
    print(token[0], token[1])
