# Contains Duplicate
def contains_duplicate(nums):
    seen= set()
    for i in nums:
        if i in seen:
            return True
        seen.add(i)    
    return False

tests = [
    [1, 2, 3, 1],   # True
    [1, 2, 3, 4],   # False
    [],             # False
    [7],            # False
    [2, 2],         # True
    [1, 1, 1, 1],   # True
]
for nums in tests:
    print(contains_duplicate(nums))