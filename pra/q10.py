# sorted square of a list 

def sorted_squares(nums):
    result = []
    left = 0
    right = len(nums) -1 
    while right >=left:
        if abs(nums[left]) > abs(nums[right]):
            result.append(nums[left] ** 2)
            left +=1
        else:
            result.append(nums[right] ** 2)
            right -=1 

    result.reverse()
    return result        

tests = [
    [-4, -1, 0, 3, 10],   # [0, 1, 9, 16, 100]
    [-7, -3, 2, 3, 11],   # [4, 9, 9, 49, 121]
    [-3, -2, -1],         # [1, 4, 9]
    [1, 2, 3],            # [1, 4, 9]
    [-3],                 # [9]
    [],                   # []
]
for nums in tests:
    print( sorted_squares(nums))