# Longest Substring Without Repeating Characters (LC 3)

# def length_of_longest(s):
#     start = 0
#     end = start+1
#     result=""
#     while end < len(s):
#         if s[end] in s[start:end]:
#             # print(f"{s[end]}, is inside ,{s[start:end]}")
#             # print("s[start:end]", s[start:end])
#             # print("s[end]", s[end])
#             if  len(s[start:end]) > len(result):
#                 result = s[start:end]
            
#             # print("posiiton",s.find(s[end] , start , end))
#             start = s.find(s[end] , start , end) + 1
#             # print('start', start)
#             # print("end", end)
            
#         end += 1  
#         if  len(s[start:end]) > len(result):
#                 result = s[start:end] 
#     return len(result)


def length_of_longest(s):
    last = {}              # character -> its last index
    start = 0
    best = 0
    for end, ch in enumerate(s):
        if ch in last:
            start = max(start, last[ch] + 1) 
        last[ch] = end 
        best = max(best, end - start + 1)  # count after every step
    return best

tests = [
    "abcabcbb",   # 3
    "bbbbb",      # 1
    "pwwkew",     # 3
    "",           # 0
    " ",          # 1
    "abba",       # 2
    "dvdf",       # 3
    "tmmzuxt",    # 5
]

for s in tests:
    print(repr(s), "->", length_of_longest(s))