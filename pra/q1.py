stock = [7, 1, 5, 3, 6, 4]


def max_profit(prices):
    best = 0 
    lowest = float("inf")
    for i in prices:
        lowest = min(lowest, i)
        best = max(best, i - lowest)
    
    return best

x = max_profit(stock)
print(x)