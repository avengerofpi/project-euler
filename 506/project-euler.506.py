#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict
import scipy
import numpy
from numpy import array

# Tests
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected
TESTS = [
    TestCase(11, 36120),
    TestCase(1000, 18232686),
    #TestCase(10 ** 8, "UNKNOWN"),
]

# Constants
baseStr = "123432"
lenBaseStr = len(baseStr)
clockSpokes = [
        1,     2,     3,     4,    32,
      123,    43,  2123,   432,  1234,
    32123, 43212, 34321, 23432, 123432
]
clockSpokeSizes = [len(str(spoke)) for spoke in clockSpokes]
clockWheel = [
    123432,
    234321,
    343212,
    432123,
    321234,
    123432,
    432123,
    212343,
    432123,
    123432,
    321234,
    432123,
    343212,
    234321,
    123432,
]

clockLen = len(clockSpokes)
clockSpokeSum = sum(clockSpokes)
MODULUS = 123454321

# Logging 
info = True
debug = False
verbose = True
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)

# Functions
def S(N):
    logDebug(f"Computing S({N})")
    total = 0
    if N <= clockLen:
        total += sum(clockSpokes[0:N])
    else:
        k = N // clockLen
        total += clockSpokeSum * k
        total += sum(clockWheel[a] * sum(sum(10**(6*j) for j in range(i)) for i in range(k)) * (10**clockSpokeSizes[a]) for a in range(clockLen))

        q = N % clockLen
        total += sum(clockSpokes[0:q])
        total += sum(clockWheel[a] * sum(10**(6*i) for i in range(k)) * (10**clockSpokeSizes[a]) for a in range(q))
        logVerbose(f"  k = {k}, q = {q}")

    logDebug(f"Total for N={N}: {total}")
    return total

def SwithMod(N):
    return S(N) % MODULUS

def runTests():
    for test in TESTS:
        N = test.N
        expected = test.expected
        logInfo(f"Running against N = {N}", flush=True)

        ans = SwithMod(N)
        successStr = "SUCCESS" if (ans == expected) else f"FAILURE (expected {expected})"
        logInfo(f"{N}: {ans} - {successStr}")
        logInfo()

def troubleshoot():
    prev = 0
    for N in range(1,40):
        t = S(N)
        d = t - prev
        try:
            sumD = sum(int(c) for c in str(d))
        except:
            sumD = "unknown"
        logInfo(f"S({N:2}) = {t:20} - diff: {d:20} (sum: {sumD:5})")
        prev = t

# Main logic
def main():
    #troubleshoot()
    logInfo()

    runTests()

# Main logic
if __name__ == '__main__':
    main()
