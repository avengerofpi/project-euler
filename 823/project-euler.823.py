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
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, N, numIters, expected, period = UNKNOWN, periodStart = UNKNOWN):
        self.N = N
        self.numIters = numIters
        self.expected = expected
        self.period = period
        self.periodStart = periodStart

TESTS = [
    TestCase(5, 3, 21),
    TestCase(5, 10, 19, 3, 4),
    TestCase(10, 100, 257, 20, 9),
    TestCase(10, 101, 175, 20, 9),
    TestCase(10, 1000, 257, 20, 9),
    TestCase(10, 1001, 175, 20, 9),
    TestCase(100, 1000, 989136573),
    TestCase(100, 10**6, UNKNOWN),
    TestCase(1000, 10000, 204600045),
    TestCase(1000, 100000, 803889757),
    # require too much memory atm
    TestCase(1000, 1000000, UNKNOWN),
    #TestCase(a, b, "UNKNOWN"),
]

# Constants
MOD = 1234567891

# Logging
info = True
debug = False
verbose = False
timing = True
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
    # The first list will not be seen again, so don't bother adding it
    seenToIndexMap = defaultdict(int)
    period = UNKNOWN
    periodStart = UNKNOWN
    for i in range(1, numIters+1):
        currList = nextList(currList)
        logList(currList, i)
        currTuple = tuple(tuple(e) for e in currList)
        prevIndex = seenToIndexMap[currTuple]
        if prevIndex:
            periodStart = prevIndex
            period = i - prevIndex
            remainingIters = numIters - i
            loopsToSkip = remainingIters // period
            itersAfterLooping = remainingIters % period
            finalIndex = prevIndex + itersAfterLooping
            for aList, aIndex in seenToIndexMap.items():
                if aIndex == finalIndex:
                    finalList = aList
            logInfo(f"---------- THIS ENTRY HAS BEEN SEEN BEFORE ----------")
            logInfo(f"  periodStart        {periodStart}")
            logInfo(f"  currIndex          {i}")
            logInfo(f"  period             {period}")
            logInfo(f"  remainingIters     {remainingIters}")
            logInfo(f"  loopsToSkip:       {loopsToSkip}")
            logInfo(f"  itersAfterLooping: {itersAfterLooping}")
            logInfo(f"  finalIndex:        {finalIndex}")
            logInfo(f"  finalList:         {finalList}")
            logInfo(f"-----------------------------------------------------")

            currList = finalList
            break
        else:
            seenToIndexMap[currTuple] = i
    prodList = transformFactoredListIntoProductList(currList)
    finalSum = sum(prodList)
    logInfo(f"S({n}, {numIters}) -> {prodList} -> {finalSum}")

    return finalSum, period, periodStart

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        numIters = test.numIters
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ansBeforeMod, period, periodStart = runFactorShuffle(N, numIters)
        logInfo(f"period(n = {N:6d}) = {period:6} (starts at {periodStart:6}) (final sum after {numIters} rounds: {ansBeforeMod}")
        ans = ansBeforeMod % MOD
        if ans == UNKNOWN:
            successStr = UNKNOWN
        elif ans == expected:
            successStr = "SUCCESS"
        else:
            successStr = f"FAILURE (expected {expected})"
        logInfo(f"Result for {N} after {numIters} rounds: {ans} - {successStr}")

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()

def troubleshoot():
    for n in range(3, 100):
        numIters = 10 ** 8
        finalSum, period, periodStart = runFactorShuffle(n, numIters)
        logInfo(f"period(n = {n:6d}) = {period:6d} (starts at {periodStart:6}) (final sum after {numIters} rounds: {finalSum}")

# Main logic
def main():
    #troubleshoot()
    runTests()

# Main logic
if __name__ == '__main__':
    main()
