#!/usr/bin/env python3

# Imports

# Functions
def rev(k):
    return int(''.join(reversed(str(k))))

def one_round(k):
    return k + rev(k)

def is_palindrome(k):
    return k == rev(k)

# Main logic
cnt = 0
for i in range(1, 10001):
    n = i
    for j in range(50):
        if j == 49:
            cnt += 1
            print(f"{i} | Lychrel")
            break
        n = one_round(n)
        if is_palindrome(n):
            print(f"{i} | {j+1} rounds")
            break
print(f"Num Lychrel Numbers less than 10k: {cnt}")
