# Remove Duplicates from Sorted Array (LeetCode 26)

def remove_duplicates(nums):
    position = 0 
    for i  in range(0 , len(nums) -1):
        if nums[i+1] != nums[i]:
            nums[position + 1] = nums[i+1]
            position += 1 

    return (position+1)

nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]

print(remove_duplicates(nums))