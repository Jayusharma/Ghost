# Valid Parentheses (LC 20)

def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}   # closer -> its opener
    stack = []
    for ch in s:
        if ch in pairs:                          # a closing bracket
            if not stack or stack[-1] != pairs[ch]:
                return False                     # nothing to close, or wrong type on top
            stack.pop()                          # matched, remove the opener
        else:                                    # an opening bracket
            stack.append(ch)
    return not stack




tests = [
    "()",        # True
    "()[]{}",    # True
    "(]",        # False
    "([)]",      # False
    "{[]}",      # True
    "(",         # False
    ")",         # False
    "((",        # False
    "([]",       # False
]

for s in tests:
    print(repr(s), "->", is_valid(s))