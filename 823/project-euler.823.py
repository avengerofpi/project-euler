#!/usr/bin/python3

# Imports
from math import log, log2, log10, prod, sqrt
from collections import defaultdict
import scipy
import numpy
from numpy import array
from datetime import timedelta
import time
#pip3 install primefac
from primefac import primefac

# Tests
class TestCase:
    def __init__(self, N, numIters, expected):
        self.N = N
        self.numIters = numIters
        self.expected = expected

TESTS = [
    TestCase(5, 3, 21),
    TestCase(10, 100, 257),
    TestCase(10, 101, 175),
    TestCase(10, 1000, 257),
    TestCase(10, 1001, 175),
    TestCase(100, 1000, 989136573),
    TestCase(1000, 10000, 204600045),
    #TestCase(a, b, "UNKNOWN"),
]

# Constants
MOD = 1234567891

# Logging
info = True
debug = False
verbose = False
timing = False
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)
def logTiming(msg = ""):
    if timing:
        print(msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def logList(currList, iterNum):
    width = 3
    logDebug(f"  {iterNum:{width}d}: {transformFactoredListIntoProductList(currList)}")
    for e in currList:
        v = prod(e)
        logVerbose(f" {' ' * width}... {e}")

def transformFactoredListIntoProductList(currList):
    return [prod(e) for e in currList]

def transformRange(n):
    return list(list(primefac(i)) for i in range(2,n+1))

def nextList(currList):
    nextE = []
    nextList = []
    for e in currList:
        p = e[0]
        nextE.append(p)
        if len(e) > 1:
            e = e[1:]
            nextList.append(e)
    nextE.sort()
    nextList.append(nextE)
    return nextList

def runFactorShuffle(n, numIters):
    logInfo(f"Running for n = {n}, {numIters} rounds:")
    currList = transformRange(n)
    logList(currList, 0)
    for i in range(1, numIters+1):
        currList = nextList(currList)
        logList(currList, i)
    prodList = transformFactoredListIntoProductList(currList)
    finalSum = sum(prodList)
    logInfo(f"S({n}, {numIters}) -> {prodList} -> {finalSum}")

    return finalSum

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        numIters = test.numIters
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ansBeforeMod = runFactorShuffle(N, numIters)
        ans = ansBeforeMod % MOD
        successStr = "SUCCESS" if (ans == expected) else f"FAILURE (expected {expected})"
        logInfo(f"{N}: {ans} - {successStr}")

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()

def troubleshoot():
    runFactorShuffle(5, 3)
    runFactorShuffle(10, 100)

# Main logic
def main():
    #troubleshoot()

    runTests()

# Main logic
if __name__ == '__main__':
    main()
