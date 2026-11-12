# check if its palindrom 

def is_palindrome(s):
    clean = [ch.lower() for ch in s if ch.isalnum()]
    
    left = 0 
    right = len(clean) - 1
    while right > left:
        # print(f"{clean[left]} and {clean[right]}")
        if clean[left] == clean[right]:
            left +=1
            right -=1
        else:
            return False
    
    return True 

tests = ["A man, a plan, a canal: Panama", "race a car", "", ".,", "a.", "0P"]

for t in tests:
    print(is_palindrome(t))
