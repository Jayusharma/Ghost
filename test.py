print([n * 2 for n in [1, 2, 3, 4] if n % 2 == 0])
print(["even" if n % 2 == 0 else "odd" for n in range(3)])
print({n: n * n for n in range(3)})
g = (n * n for n in range(3))
print(list(g))
print(list(g))
x = 10
nums = [x for x in range(3)]
print(x)