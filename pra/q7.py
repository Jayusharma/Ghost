# Sum of two numbers in a unorderd list 

def two_sum(nums, target):
    pair={}
    for i , n in enumerate(nums):
        x = target - n
        if x in pair:
            y = pair.get(x)
            return (y , i)
        pair[n] = i    
    return None



tests = [
    ([2, 7, 11, 15], 9),    # (0, 1)
    ([3, 2, 4], 6),       # (1, 2)
    ([3, 3], 6),            # (0, 1)
    ([5], 10),              # None
    ([1, 2, 3], 100),       # None
    ([], 5),                # None
]
for nums, target in tests:
    print(two_sum(nums, target))