# # monotonic array 

nums = [3 , 2 , 4]
# def check_monotonic(numbers):

#     y = numbers[1] - numbers[0]
#     if y >= 0:
#         x = 1
#     else:
#         x = 0

#     for i in range(1 , len(numbers)-1 ):
#         z = numbers[i+1] - numbers[i]
#         if x == 1 and z < 0:
#             return False
#         elif x == 0 and z > 0:
#             return False
    
#     return True
            
# final = check_monotonic(nums)
# print(final)


def is_monotonic(nums):
    increasing = True
    decreasing = True
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            decreasing = False
        if nums[i] < nums[i - 1]:
            increasing = False
    return increasing or decreasing

final = is_monotonic(nums)
print(final)