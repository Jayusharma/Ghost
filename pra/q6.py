# two sum of the sorted array 

def two_sum_sorted(nums, target):
    left = 0
    right = len(nums) - 1
    
    while right > left:
        if nums[left] + nums[right] == target:
            return (left , right)
        elif nums[left] + nums[right] > target:
            right -=1 
        else:
            left +=1         

    return None

tests = [
    ([2, 7, 11, 15], 9),    # (0, 1)
    ([2, 7, 11, 15], 18),   # (1, 2)
    ([1, 2, 3, 4], 7),      # (2, 3)
    ([3, 3], 6),            # (0, 1)
    ([1, 2, 3], 100),       # None
    ([], 5),                # None
]
for nums, target in tests:
    print(two_sum_sorted(nums, target))