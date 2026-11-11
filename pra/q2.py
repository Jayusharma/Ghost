# max consective days

days = [1]

def max_days(days):
    count = 0 
    best = 0 
    for i in range(len(days)):
        if days[i] == 1:
            count += 1
            best = max(best , count)
        else:
            count = 0

    
    return best

x = max_days(days)
print(x)