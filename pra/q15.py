# Group Anagrams (LeetCode 49)

from collections import Counter, defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for word in strs:
        key = tuple(sorted(Counter(word)))
        print(key)
        groups[key].append(word)
    return list(groups)

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
