#!/usr/bin/env python3

# Imports
from collections import defaultdict
from datetime import timedelta
import time
from colorama import Fore, Back, Style

# Tests
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, n, expected):
        self.n = n
        self.expected = expected

class TestCaseCollections:
    def __init__(self):
        self.BASE = [
            TestCase(1, 1),
            TestCase(1, 2),
            TestCase(2, 3),
            TestCase(3, 5),
            TestCase(4, 6),
            TestCase(6, 10),
            TestCase(7, 11),
            TestCase(8, 14),
            TestCase(9, 16),
            TestCase(10, 18),
            TestCase(100, 415),
            TestCase(10000, 312807),
        ]
        self.CHALLENGES = [
            TestCase(10**13, UNKNOWN),
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

def printTestResult(tc, result):
    RESET_COLOR = Style.RESET_ALL

    expected = tc.expected
    n = tc.n
    ans = result.expected
    if ans == expected:
        successStr = "SUCCESS"
        b = Back.GREEN
        c = Fore.RED
    else:
        if expected == UNKNOWN:
            successStr = f"FAILURE (expected {expected} but got {ans})"
        else:
            successStr = f"FAILURE (expected {expected} but got {ans})"
        b = Back.RED
        c = Fore.YELLOW
    logInfo(f"{c}{b} Result for {tc.n}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")
    logInfo(f"{c}{b}TestCase({tc.n}, {result.expected}),{RESET_COLOR}")

def get_fib_up_to_n(n):
    if n < 1:
        return []
    if n == 1:
        return [1]
    fib = [1, 2]
    logDebug(f"get_fib_up_to_n({n})")
    while (f := sum(fib[-2:])) and f <= n:
        fib.append(f)
        logDebug(f"  {f}: {fib}")
    logDebug(f"get_fib_up_to_n({n}) has {len(fib)} elements")
    logDebug("")
    return fib

def not_zeckendorf(n):
    fib = get_fib_up_to_n(n)
    from collections import defaultdict
    sum_tuples = defaultdict(list)
    sum_tuples[0] = [tuple()]
    for f in fib:
        logDebug(f"{f}")
        for s, tt in list(reversed(sum_tuples.items())):
            logDebug(f"  {s}={tt} (existing values)")
            for t in tt:
                if s+f <= n:
                    sum_tuples[s+f].append(t + (f,))
                    logDebug(f"    {s+f}={sum_tuples[s+f]} (appended)")
        logDebug(f"  {sorted(sum_tuples.items())}")
        logDebug(f"{f}")
        for s, tt in sorted(sum_tuples.items()):
           if s > n:
               continue
           logDebug(f"  {s}")
           for t in tt:
               logDebug(f"    {t}")
    total = sum(len(tt) for s, tt in sum_tuples.items() if s <= n)
    return total

def runTests(tests):
    for test in tests:
        startTime = getTimeInMillis()
        n = test.n
        logInfo(f"Running against n = {n}")

        ans = not_zeckendorf(n)
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
    tests = testCaseCollections.BASE #+ testCaseCollections.CHALLENGES
    runTests(tests)

# Main logic
if __name__ == '__main__':
    main()
