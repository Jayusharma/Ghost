# First Unique Character in a String (LC 387)
from collections import Counter
# method one 
def unique_char(strs):
    
    counts = {} 
    for i , value in enumerate(strs):
         pair = counts.get(value, [0, i])
         pair[0] += 1
         counts[value] = pair
    
    for value in counts:
        # print(i , value , counts.get(value)[0] )
        if counts.get(value)[0] == 1:
            return counts.get(value)[1]
            
    return -1

# Method 2 
def unique_char(s):
    counts = Counter(s)              # pass 1: count every letter
    for i, ch in enumerate(s):       # pass 2: walk the string in its real order
        if counts[ch] == 1:
            return i                 # first hit is the earliest unique one
    return -1   

strs = "aabc"

print(unique_char(strs))