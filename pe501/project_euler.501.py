#!/usr/bin/env python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict
from datetime import timedelta
import time

# Constants
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(100, 10),
    TestCase(1000, 180),
    TestCase(10 ** 6, 224427),
    TestCase(10 ** 7, "UNKNOWN"),
    TestCase(10 ** 8, "UNKNOWN"),
#    TestCase(10 ** 9, "UNKNOWN"),
#    TestCase(10 ** 10, "UNKNOWN"),
#    TestCase(10 ** 11, "UNKNOWN"),
#    TestCase(10 ** 12, "UNKNOWN"),
]

# Logging 
info = True
debug = True
verbose = False
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as some collection object.

    This is a simple seive generator, nothing fancy.
    """
    primes = []
    checkPrimesI = 0
    if N >= 2:
        primes.append(2)
        for candidateP in range(3, N+1, 2):
            while ((checkPrimesI < len(primes) - 1) and (primes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in primes[0:checkPrimesI + 1]):
                primes.append(candidateP)
    return tuple(primes)

# Main logic
def main():
    for test in TESTS:
        startTime = getTimeInMillis()
        
        N = test.N
        expected = test.expected

        logInfo(f"Running against N = {N}")
        primeBound = N // 6
        primes = computePrimesUpToN(primeBound)
        logDebug(f"  Computing primes up to {primeBound} - found {len(primes)} from {primes[0]} to {primes[-1]}")

        p7Count = 0
        p3qCount = 0
        pqrCount = 0

        logDebug(f"Checking for n = p ** 7")
        for p in primes:
            p7 = p ** 7
            if p7 <= N:
                p7Count += 1
            else:
                break

        logDebug(f"Checking for n = p**3 * q")
        for p in primes:
            p3 = p ** 3
            if N <= p3:
                break
            for q in primes:
                if p == q:
                    continue
                p3q = p3 * q
                if p3q <= N:
                    p3qCount += 1
                else:
                    break

        logDebug(f"Checking for n = p * q * r")
        for p in primes:
            for q in primes:
                if q <= p:
                    continue
                pq = p * q
                if N <= pq * q:
                    break
                for r in primes:
                    if r <= q:
                        continue
                    pqr = pq * r
                    if pqr <= N:
                        pqrCount += 1
                    else:
                        break

        logDebug(f"  Found {p7Count} numbers of the form p**7")
        #if verbose:
        #    for (p,p7) in p7List:
        #        logVerbose(f"    {p:4}**7= {p7:8}")
        logDebug(f"  Found {p3qCount} numbers of the form p**3 * q")
        #if verbose:
        #    for (p,q,p3q) in p3qList:
        #        logVerbose(f"    {p:4}**3 * {q:4} = {p3q:8}")
        logDebug(f"  Found {pqrCount} numbers of the form p * q * r")
        #if verbose:
        #    for (p,q,r, pqr) in pqrList:
        #        logVerbose(f"    {p:4} * {q:4} * {r:4} = {pqr:8}")
        ans = p7Count + p3qCount + pqrCount
        successStr = "SUCCESS" if (ans == expected) else f"FAILURE (expected {expected})"
        logInfo(f"{N}: {ans} - {successStr}")

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime 
        logDebug(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

        logInfo("")


# Main logic
if __name__ == '__main__':
    main()
