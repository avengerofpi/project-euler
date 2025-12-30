#!/usr/bin/env python3

# Imports
from math import log, log2, log10, prod, sqrt
from collections import defaultdict
import scipy
import numpy
from numpy import array
from datetime import timedelta
import time

# Tests
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected
TESTS = [
    TestCase(     11,     36120),
    TestCase(    100,   9291482),
    TestCase(   1000,  18232686),
    TestCase(   2000,  65456260),
    TestCase(  10000, 107644726),
    TestCase(  20000,   6116055),
    TestCase(10 ** 5,  14130558),
    TestCase(10 ** 6,  66623446),
    TestCase(10 ** 7,  97735042),
    TestCase(10 ** 8,  38488039),
    TestCase(10 ** 9,  63289614),
    TestCase(10 ** 10, "UNKNOWN"),
    TestCase(10 ** 11, "UNKNOWN"),
    TestCase(10 ** 12, "UNKNOWN"),
    TestCase(10 ** 13, "UNKNOWN"),
    TestCase(10 ** 14, "UNKNOWN"),
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
# memoModBinaryPowersOfTen[i] = 10**{2**i} mod MODULUS
memoModBinaryPowersOfTen = { 0: 10 }
# Uses up a bunch of memory for larger test cases
memoModPowersOfTen = { }
maxN = max(testCase.N for testCase in TESTS)
logMaxN = int(log2(maxN)) + 1
for i in range(1, logMaxN):
    memoModBinaryPowersOfTen[i] = memoModBinaryPowersOfTen[i-1]**2 % MODULUS
    logVerbose(f"memoModBinaryPowersOfTen[{i}] = 10**{2**i} = {memoModBinaryPowersOfTen[i]}")
def modPowersOfTen(n):
    try:
        return memoModPowersOfTen[n]
    except:
        # e.g., n = 23 -> 0b10111 -> 10111 -> ['1', '0', '1', '1', '1'] -> ['1', '1', '1', '0' '1']
        #                            abcde -> ['a', 'b', 'c', 'd', 'e'] -> ['e', 'd', 'c', 'b' 'a']
        binN = bin(n)
        binN = list(bin(n)[2:])
        binN.reverse()
        t = 1
        for i in range(len(binN)):
            if binN[i] == '1':
                p = memoModBinaryPowersOfTen[i]
                t = t * p
        t = t % MODULUS
        memoModPowersOfTen[n] = t
        #time.sleep(1)
        return t

memoSumPowersOfTen = { 0: 0, 1: 1 }
def modSumPowersOfTen(n):
    try:
        return memoSumPowersOfTen[n]
    except:
        m = (memoSumPowersOfTen[n-1] + modPowersOfTen(6*(n-1))) % MODULUS
        memoSumPowersOfTen[n] = m
        return m

def S(N):
    logDebug(f"Computing S({N})")
    total = 0
    if N <= clockLen:
        total += sum(clockSpokes[0:N])
    else:
        k = N // clockLen
        total += clockSpokeSum * k
        for a in range(clockLen):
            for i in range(k):
                inc = clockWheel[a] * modSumPowersOfTen(i) * modPowersOfTen(clockSpokeSizes[a])
                total = (inc + total) % MODULUS

        q = N % clockLen
        total += sum(clockSpokes[0:q])
        for a in range(q):
            inc = clockWheel[a] * modSumPowersOfTen(k) * modPowersOfTen(clockSpokeSizes[a])
            total = (inc + total) % MODULUS
        logVerbose(f"  k = {k}, q = {q}")

    logDebug(f"Total for N={N}: {total}")
    return total

def SwithMod(N):
    return S(N) % MODULUS

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ans = SwithMod(N)
        successStr = "SUCCESS" if (ans == expected) else f"FAILURE (expected {expected})"
        logInfo(f"{N}: {ans} - {successStr}")

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logDebug(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
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
