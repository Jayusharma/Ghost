# Reserve the list without using reserve or other shortcuts


def reverse_in_place(nums):
    left = 0
    right = len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
        print(nums)

for case in [[1, 2, 3, 4, 5], [1, 2, 3, 4], [7], []]:
    reverse_in_place(case)
    print(case)