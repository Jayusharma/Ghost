# Longest Consecutive Sequence (LC 128)


# def longest_consecutive(nums):
#     x = sorted(nums)
#     start = 0
#     best = 0
#     for end in range(1 , len(x) ):
#         print("start", start , "and end is " , end)
#         print("end is ",x[end])
#         if x[end] - x[end-1] != 1:
#             print("its not consecutive")
#             start = end 
        
#         best = max(best , end-start + 1)   
#         print("best", best)     
#     return best


# def longest_consecutive(nums):
#     my_set = set(nums)    
#     x = sorted(my_set)   
#     start = 0
#     best = 1
#     for end in range(1 , len(x)):
#         if x[end] - x[end-1] > 1:
#             start = end 

#         best = max(best , end-start + 1)
#     return best


def longest_consecutive(nums):
    num_set = set(nums)
    best = 0
    for v in num_set:
        if v - 1 not in num_set:          # v is the start of a run
            length = 1
            while v + length in num_set:  # walk up the run
                length += 1
            best = max(best, length)
    return best

    
tests = [
    [100, 4, 200, 1, 3, 2],               # 4
    [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],       # 9
    [1, 0, 1, 2],                         # 3
    [],                                   # 0
    [5],                                  # 1
    [1, 1, 1],                            # 1
    [-1, -2, -3, 10],                     # 3
    [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],  # 7
]

for nums in tests:
    print(nums, "->", longest_consecutive(nums))