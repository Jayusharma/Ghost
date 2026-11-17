# Top K Frequent Elements (LC 347)
from collections import Counter
import heapq

# def frequent_elements(nums , k):
#     counts = Counter(nums)
#     y = sorted(counts.items() , key=lambda p: p[1] , reverse=True )[:k]
#     return [p[0] for p in y]    

def frequent_elements(nums, k):
    counts = Counter(nums)                          # Phase 1
    heap = []
    for num, count in counts.items():               # Phase 2
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for count, num in heap] 



tests = [
    ([1, 1, 1, 2, 2, 3],              2),   # [1, 2]
    ([1],                             1),   # [1]
    ([5, 5, 5, 5],                    1),   # [5]
    ([4, 1, -1, 2, -1, 2, 3],         2),   # [-1, 2]
    ([0, 0, 0, -3, -3, 7],            1),   # [0]
    ([1, 2, 3],                       3),   # [1, 2, 3]
    ([3, 3, 3, 3, 2, 2, 2, 1, 1, 5],  3),   # [3, 2, 1]
    ([-5, -5, -1],                    1),   # [-5]
]


for nums , k in tests:
    print("ansers",frequent_elements(nums , k))
    # frequent_elements(nums , k)