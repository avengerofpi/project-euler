#!/usr/bin/env python3

# Imports

# Functions
def tNumber(n):
    return n*(  n+1)//2

def pNumber(n):
    return n*(3*n-1)//2

def hNumber(n):
    return n*(2*n-1)

# Main logic
PRECOMPUTE_LEN = 100000
tNumbers = [tNumber(i) for i in range(1, PRECOMPUTE_LEN+1)]
pNumbersSet = set([pNumber(i) for i in range(1, PRECOMPUTE_LEN+1)])
hNumbersSet = set([hNumber(i) for i in range(1, PRECOMPUTE_LEN+1)])
bothPandH = pNumbersSet.intersection(hNumbersSet)

for index in range(PRECOMPUTE_LEN):
    i = index+1
    t = tNumbers[index]
    if (t in bothPandH):
        print(f"{i} -> {t}")

