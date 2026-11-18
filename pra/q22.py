# Next: Container With Most Water (LC 11)

def max_area(h):
    i, j = 0, len(h) - 1
    best = 0
    while i < j:
        area = min(h[i], h[j]) * (j - i)
        best = max(best, area)
        if h[i] <= h[j]:
            i += 1
        else:
            j -= 1
    return best

tests = [
    [1, 8, 6, 2, 5, 4, 8, 3, 7],   # 49
    [1, 1],                        # 1
    [4, 3, 2, 1, 4],               # 16
    [1, 2, 1],                     # 2
    [0, 2, 0],                     # 0
    [2, 3, 4, 5, 18, 17, 6],       # 17
    [5, 5, 5, 5],                  # 15
    [1, 2, 4, 3],                  # 4
]

for h in tests:
    print(h, "->", max_area(h))