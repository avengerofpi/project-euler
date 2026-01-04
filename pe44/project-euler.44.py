#!/usr/bin/env python3

# Imports

# Functions
def pentagonalNumber(n):
    return n*(3*n-1)//2

# Main logic
PRECOMPUTE_LEN = 10000
pentagonalNumbers = [pentagonalNumber(i) for i in range(1, PRECOMPUTE_LEN+1)]
asSet = set(pentagonalNumbers)

validPairs = []
for i in range(1, PRECOMPUTE_LEN):
    for j in range(i+1, PRECOMPUTE_LEN):
        iValue = pentagonalNumbers[i]
        jValue = pentagonalNumbers[j]
        s = jValue + iValue
        d = jValue - iValue
        if ((s in asSet) and (d in asSet)):
            validPair = (i, j)
            validPairValues = (iValue, jValue)
            validPairs.append(validPair)
            print(f"{validPair} -> {validPairValues} -> {d}")

