#!/usr/bin/env python3

# Imports
from datetime import timedelta
import time
from colorama import Fore, Back, Style
from math import gcd

from functools import reduce
from operator import xor

# Tests
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, n, expected):
        self.n = n
        self.expected = expected

class TestCaseCollections:
    def __init__(self):
        self.BASE = [
            TestCase(1, 1/2),
            TestCase(2, 3/8),
            TestCase(3, 7/24),
            TestCase(4, 1/4),
            TestCase(6, 0.1916666666667),
            TestCase(7, 0.1666666666667),
            TestCase(8, 0.1535714285714),
            TestCase(9, 0.139880952381),
            TestCase(10, 0.1319444444444),
        ]
        self.CHALLENGES = [
            TestCase(20, 0.076648811285),
            TestCase(100, 0.0204893783592),
            TestCase(1000, 0.002751455605),
            # TestCase(10**4, UNKNOWN),  # 10.5 sec
            TestCase(35000, 0.0001095147945),  # 2 min, 13 sec
            # TestCase(10**5, 0.0000415216278),  # 18 min, 46 sec
        ]

# Constants
ROUNDING_DIGITS = 13
ALLOWED_ERROR = 10**(-13) / 2

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

def printTestResult(tc, result):
    PATH_COLOR = Fore.RED
    RESET_COLOR = Style.RESET_ALL

    expected = tc.expected
    n = tc.n
    ans = result.expected
    if expected != UNKNOWN and abs(ans - expected) < ALLOWED_ERROR:
        successStr = "SUCCESS"
        b = Back.GREEN
        c = Fore.RED
    else:
        if expected == UNKNOWN:
            successStr = f"FAILURE (expected {expected} but got {ans:0.{ROUNDING_DIGITS}f})"
        else:
            successStr = f"FAILURE (expected {expected:0.{ROUNDING_DIGITS}f} but got {ans:0.{ROUNDING_DIGITS}f})"
        b = Back.RED
        c = Fore.YELLOW
    logInfo(f"{c}{b} Result for {tc.n}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")
    logInfo(f"{c}{b}TestCase({tc.n}, {result.expected}),{RESET_COLOR}")

def sum_of_minimal_triangles(n):
    total = 0
    for i in range(n//2 + 1, n+1):
        logDebug(f"Pairs for i = {i}")
        for j in range(n+1-i, i):
            if gcd(i, j) == 1:
                logDebug(f"  ({i}, {j})")
                total += 1/(i*j) * (1/i + 1/j)
    total = total / 2

    return total

def runTests(tests):
    for test in tests:
        startTime = getTimeInMillis()
        n = test.n
        logInfo(f"Running against n = {n}")

        ans_before_rounding = sum_of_minimal_triangles(n)
        ans = round(ans_before_rounding, ROUNDING_DIGITS)
        result = TestCase(n, ans)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()
        logInfo()
        logInfo()

# Main logic
def main():
    #troubleshoot()

    testCaseCollections = TestCaseCollections()
    tests = testCaseCollections.BASE + testCaseCollections.CHALLENGES
    runTests(tests)

# Main logic
if __name__ == '__main__':
    main()
