# smallest distance from k point

import heapq 

def k_closest_sorted(points , k):
    heap = [(x**2 + y**2 , x , y ) for x , y in points]
    heapq.heapify(heap)
    result = []
    for t in range(k):
        d, x ,y = heapq.heappop(heap)
        result.append([x , y])
    return result    


tests = [
    ([[1, 3], [-2, 2]], 1),               # [[-2, 2]]
    ([[3, 3], [5, -1], [-2, 4]], 2),      # [[3, 3], [-2, 4]]
    ([[0, 1], [1, 0]], 2),                # both points
    ([[1, 1]], 1),                        # [[1, 1]]
    ([[2, 2], [-2, -2], [1, 1]], 1),      # [[1, 1]]
    ([[0, 0], [1, 1], [2, 2]], 2),        # [[0, 0], [1, 1]]
]
for points, k in tests:
    print(k_closest_sorted(points, k))