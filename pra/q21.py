# Daily Temperatures (LC 739)


def daily_temperatures(temps):
    n = len(temps)
    answer = [0] * n
    stack = []                                    # indices of days still waiting
    for i in range(n):
        while stack and temps[i] > temps[stack[-1]]:
            j = stack.pop()                       # day j just found its warmer day
            answer[j] = i - j                     # the distance in days
        stack.append(i)                           # day i now waits
    return answer



tests = [
    [73, 74, 75, 71, 69, 72, 76, 73],           # [1, 1, 4, 2, 1, 1, 0, 0]
    [30, 40, 50, 60],                           # [1, 1, 1, 0]
    [30, 60, 90],                               # [1, 1, 0]
    [90, 80, 70],                               # [0, 0, 0]
    [50],                                       # [0]
    [70, 70, 70],                               # [0, 0, 0]
    [60, 50, 70, 55, 65],                       # [2, 1, 0, 1, 0]
    [89, 62, 70, 58, 47, 47, 46, 76, 100, 70],  # [8, 1, 5, 4, 3, 2, 1, 1, 0, 0]
]

for t in tests:
    print(t, "->", daily_temperatures(t))