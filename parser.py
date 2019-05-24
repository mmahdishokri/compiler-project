from scanner import get_next_token
from constant import *

stack = [start]
while stack[-1] != end:
    token = next_token()
    state = stack[-1]
    go[state][terminal] = state2
    Go[state][non_terminal] = state2



print("Hello! I am your parser ^_^")

code = open("code.c", "r")
output_file = open("parser.txt", "w")
error_file = open("parse_errors.txt", "w")

tokens = []
errors = []
state = 0
word_wrapper = [""]
line_number_wrapper = [1]

while state != EOF:
    state = get_next_token(state, word_wrapper, line_number_wrapper, tokens, errors)
    print("state = ", state)
    print("word = ", word_wrapper[0])
    print("tokens =", tokens)
    print("errors = ", errors)
