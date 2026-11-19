# binary search 

# def linear_search(nums , target):
#     for i , ch in enumerate(nums):
#         if ch == target:
#             return i 
#     return -1

def binary_search(nums , target):
    i = 0 
    j = len(nums) -1
    while i <= j:
        # print(f"i is {i} and j is {j}")
        middle = (i + j)//2
        # print("middle" , middle)
        if target == nums[middle]:
            return middle
        elif target > nums[middle]:
            i = middle + 1
        else:
            j = middle - 1
            
    return -1   

tests = [
    ([-1, 0, 3, 5, 9, 12], 9),       # 4
    ([-1, 0, 3, 5, 9, 12], 2),       # -1
    ([5], 5),                        # 0
    ([5], 3),                        # -1
    ([1, 3], 3),                     # 1
    ([1, 3], 1),                     # 0
    ([1, 2, 3, 4, 5, 6, 7], 7),      # 6
    ([1, 2, 3, 4, 5, 6, 7], 1),      # 0
    ([1, 2, 3, 4, 5, 6, 7], 0),      # -1
    ([1, 2, 3, 4, 5, 6, 7], 8),      # -1
    ([2, 4, 6, 8], 5),               # -1
]

for nums, target in tests:
    print(nums, target, "->", binary_search(nums, target))