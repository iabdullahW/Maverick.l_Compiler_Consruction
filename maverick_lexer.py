"""
Maverick lexer (Python) - developed with an AI coding tool (Claude).

Maverick is a tiny line-based language: no braces, no semicolons.
Keywords: begin, finish, int, say, if, else

Token names match the Flex version (maverick.l), so both lexers print the
same output for the same input.

Run:   python maverick_lexer.py input.txt
"""
import re
import sys

KEYWORDS = {
    "begin": "M_BEGIN", "finish": "M_FINISH", "int": "M_INT",
    "say": "M_SAY", "if": "M_IF", "else": "M_ELSE",
}

OPERATORS = {
    "==": "M_EQ", "!=": "M_NE", "<=": "M_LE", ">=": "M_GE",
    "<": "M_LT", ">": "M_GT", "=": "M_ASSIGN",
    "+": "M_PLUS", "-": "M_MINUS", "*": "M_TIMES", "/": "M_DIVIDE",
    "(": "M_LPAREN", ")": "M_RPAREN",
}

# One master pattern. Order matters: comments before "/", two-character
# operators before one-character ones.
MASTER = re.compile(r"""
    (?P<COMMENT>//[^\n]*)
  | (?P<TEXT>"[^"\n]*")
  | (?P<NUMBER>[0-9]+)
  | (?P<WORD>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<OP>==|!=|<=|>=|<|>|=|\+|-|\*|/|\(|\))
  | (?P<NEWLINE>\n)
  | (?P<SPACE>[ \t\r]+)
  | (?P<BAD>.)
""", re.VERBOSE)


def tokenize(source):
    """Return a list of (line, token_name, lexeme)."""
    found = []
    line = 1
    for m in MASTER.finditer(source):
        kind, text = m.lastgroup, m.group()
        if kind == "NEWLINE":
            line += 1
        elif kind in ("SPACE", "COMMENT"):
            continue
        elif kind == "WORD":
            found.append((line, KEYWORDS.get(text, "M_NAME"), text))
        elif kind == "NUMBER":
            found.append((line, "M_NUMBER", text))
        elif kind == "TEXT":
            found.append((line, "M_TEXT", text))
        elif kind == "OP":
            found.append((line, OPERATORS[text], text))
        else:
            found.append((line, "M_ERROR", text))
    return found


def main():
    if len(sys.argv) < 2:
        print("Usage: python maverick_lexer.py input.txt")
        return
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    except OSError:
        print(f"Cannot open file {sys.argv[1]}")
        return

    tokens = tokenize(source)
    print("--- Maverick lexer ---")
    print(f"{'LINE':<5} {'TOKEN':<12} LEXEME")
    for line, name, text in tokens:
        print(f"{line:<5} {name:<12} {text}")
    errors = sum(1 for _, name, _ in tokens if name == "M_ERROR")
    print(f"--- tokens: {len(tokens) - errors}, errors: {errors} ---")


if __name__ == "__main__":
    main()
