#!/usr/bin/env python3

# Imports
from math import log, log2, log10, prod, sqrt, gcd
from collections import defaultdict
import scipy
import numpy
from numpy import add, array
from datetime import timedelta
import time
from primefac import primefac
from colorama import Fore, Back, Style
from copy import deepcopy

# Tests
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, aMax, bMax, expected):
        self.aMax = aMax
        self.bMax = bMax
        self.expected = expected

TESTS = [
    TestCase(5, 5, 15),
    TestCase(10, 10, UNKNOWN)
]

# Constants

# Logging
info = True
debug = False
verbose = False
timing = True
def logInfo(msg = ""):
    if info:
        print("INFO: " + msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print("DEBUG: " + msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print("VERBOSE: " + msg, flush=True)
def logTiming(msg = ""):
    if timing:
        print("TIME: " + msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def logValueMap(valueMap, indent=2, logger = logVerbose):
    for i in sorted(valueMap.keys()):
        v = valueMap[i]
        logger(f"{' '*indent}  {i}: {v}")

def printTestResult(tc, result):
    RESET_COLOR = Style.RESET_ALL

    expected = tc.expected
    ans = result.expected
    if expected == UNKNOWN:
        successStr = UNKNOWN
        b = Back.YELLOW
        c = Fore.RED
    elif ans == expected:
        successStr = "SUCCESS"
        b = Back.GREEN
        c = Fore.RED
    else:
        successStr = f"FAILURE (expected {expected} but got {ans})"
        b = Back.RED
        c = Fore.YELLOW
    logInfo(f"{c}{b} Result: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10})")

def runDistinctPowers(aMax, bMax):
    aToB = defaultdict(set)
    allA = set()
    aRange = range(2, aMax+1)
    bRange = range(2, bMax+1)
    
    for a in aRange:
        # Skip a that have been seen before (i.e., a perfect power of a smaller a)
        if a in allA:
            continue
        
        # base set for a
        aToB[a] = set(bRange)
        print(f"{a} ({len(aToB[a])})")
        
        # a**bBase <= bMax
        bBase = 2
        aPower = a**bBase
        while aPower <= bMax:
            print(f"  Checking a = {a}**{bBase} = {aPower}")
            ss = { bBase * b for b in bRange }
            ss = { s for s in ss if s not in aToB[a] }
            print(f"    {ss}")
            aToB[a] = aToB[a].union(ss)
            # for b in bRange:
            #     print(f"    checking b={b}")
            #     bb = aPower * b
            #     if bb > bMax:
            #         break
            #     if not bb in seen[a]:
            #         seen[a].add(aPower * b)
            #         seen[aPower].add(b)
            #
            # print(f"  {aPower} ({len(seen[aPower])}): {seen[aPower]}")
            bBase += 1
            aPower = a**bBase

    total = sum(len(aToB[a]) for a in aToB.keys())
    print(f"Total: {total}")
    return total

def runTests(tests):
    for test in tests:
        startTime = getTimeInMillis()
        aMax = test.aMax
        bMax = test.bMax
        logInfo(f"Running against (aMax, bMax) = ({aMax}, {bMax})")

        ans = runDistinctPowers(aMax, bMax)
        result = TestCase(aMax, bMax, ans)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()
        logInfo()
        logInfo()

def troubleshoot():
    return

# Main logic
def main():
    #troubleshoot()

    tests = TESTS
    runTests(tests)

# Main logic
if __name__ == '__main__':
    main()
