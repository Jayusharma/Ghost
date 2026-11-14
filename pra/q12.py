# give the kth largest number in a unsorted list 
import heapq

def kth_largest( nums , k):
    heap = []
    for n in nums:
        heapq.heappush(heap , n)
        if len(heap) >k:
            heapq.heappop(heap)
        print(heap)    
    return heap[0]        

tests = [
    ([3, 2, 1, 5, 6, 4], 4),            # 5 6 , 5 , 4 , 3
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),   # 4
    ([1], 1),                           # 1
    ([5, 5, 5], 2),                     # 5
    ([7, 6, 5, 4], 4),                  # 4
    ([2, 1], 1),                        # 2
]
for nums, k in tests:
    print(kth_largest(nums, k))