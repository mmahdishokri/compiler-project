class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        print("hereeee!")
        c = msvcrt.getch()
        print("c = " + c)
        return c


getch = _Getch()

print("Hello world!")

f = open("code.c", "r")

keywords = {'if', 'else', 'void',  'int',  'while',  'break',  'continue',  'switch',  'default',  'case',  'return'}

word = ""

while True:
    print("Here!")
    c = f.read(1)
    print('c = ' + c)
    if c == '\n':
        break
    word += c
print('word = ' + word)


def get_next_token(word):
    token = ""
    word = word + getch()
    for keyword in keywords:
        if keyword == word:
            token = keyword
    return token
