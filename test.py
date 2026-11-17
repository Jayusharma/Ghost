from collections import Counter , defaultdict

x = {}
str= "aba"
for i in str:
    x[i] = x.get(i , 0) + 1

c = Counter(x)
print (c)


print(x)    