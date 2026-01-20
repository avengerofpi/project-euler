#!/usr/bin/env python3

# Imports
from primes.generate_primes import primes_up_to_1m

# Functions

# Main logic
primes = primes_up_to_1m()
num_primes = len(primes)
max_m = 1
while sum(primes[:max_m]) < 10**6:
    max_m += 1
print(f"max_m: {max_m}")
found = False
for m in range(max_m, 1, -1):
    print(f"m = {m}")
    for a in range(max_m - m + 1):
        sub = primes[a: a+m]
        if (t := sum(sub)) and t in primes:
            print(f"{t} can be written as the sum of the {m} primes from {sub[0]} .. {sub[-1]}")
            found = True
            break
    if found:
        break
