from pyconll import load_from_string


def load_sentences(n, f):
    count = 0
    lines = ""
    line = f.readline()
    while line and count < n:
        lines += line 
        if line == "\n":
            count += 1
        line = f.readline()
    not_empty = True if line else False
    try:
        conll = load_from_string(lines)
    except Exception:
        conll = load_from_string("")
        print("bad conll")
    return conll, not_empty