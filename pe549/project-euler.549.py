#!/usr/bin/env python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict
import scipy
import numpy
from numpy import array

# Constants
debug = False
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

class TestCaseCollections:
    def __init__(self):
        self.BASE = [
            TestCase(2, 2),
            TestCase(3, 10),
            TestCase(4, 14),
            TestCase(5, 42),
            # TestCase(6, 58),
            # TestCase(7, 206),
            # TestCase(8, 326),
            # TestCase(9, 946),
            # TestCase(10, 1418),
        ]
        self.CHALLENGES = [
            TestCase(20, 1788334),
            TestCase(30, 995997524),  # 1995997531
            TestCase(32, 102083445),  # 8102083501
            # TestCase(40, UNKNOWN),  #
            # TestCase(50, UNKNOWN),
            # TestCase(60, UNKNOWN),
            # TestCase(70, UNKNOWN),
            # TestCase(80, UNKNOWN),
            # TestCase(90, UNKNOWN),
            # TestCase(100, UNKNOWN),
            # TestCase(1000, UNKNOWN),
            # TestCase(10000, UNKNOWN),
        ]

# Functions
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)

primes = []
factorization = dict()
def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as some collection object.

    This is a simple seive generator, nothing fancy.
    """
    localPrimes = []
    checkPrimesI = 0
    if N >= 2:
        localPrimes.append(2)
        for candidateP in range(3, N+1, 2):
            while ((checkPrimesI < len(localPrimes) - 1) and (localPrimes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in localPrimes[0:checkPrimesI + 1]):
                localPrimes.append(candidateP)
                #print(f"{candidateP}", flush=True)
    return tuple(localPrimes)

def factor

"""
Let s(n) be the smallest number m such that n divides m!.
Conjecture (pretty sure): If gcd(a, b) = 1, then s(a*b) = max(s(a), s(b)).
In which case, "just need to" compute s(p*k) where p is prime, k is an integer,
and p ** k <= n.
"""
def s(n):
    return 1

# Let ss(n) = sum(s(i) | 2 <= i <= n).
def ss(n):
    return sum(s(i) for i in range(1, n+1))

# Main logic
def main():
    for test in TESTS:
        N = test.N
        expected = test.expected
        primesGlobal = computePrimesUpToN(N)
        print(f"Running against N = {N}", flush=True)

        primes = computePrimesUpToN(N)

# Main logic
if __name__ == '__main__':
    main()
