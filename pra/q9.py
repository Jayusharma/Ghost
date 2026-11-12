# check for anagram 

def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if counts.get(ch, 0) == 0:
            return False          # t has more of this letter than s
        counts[ch] -= 1
    return True   


tests = [
    ("anagram", "nagaram"),   # True
    ("rat", "car"),           # False
    ("a", "ab"),              # False
    ("", ""),                 # True
    ("aab", "abb"),           # False
    ("listen", "silent"),     # True
    ("aacc", "ccac"),         # False
]
for s, t in tests:
    print(is_anagram(s, t))