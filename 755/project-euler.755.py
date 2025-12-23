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
            TestCase(10**5, 8625184),  # 0.5s (0.09s with logging commented out)
            TestCase(10**6, 236315760),  # 6s (1.04s with logging commented out)
            TestCase(10**7, 6393391136),  # 12s with logging commented out; 1.7GB memory (10.7% of 1GGB)
            TestCase(5*10**7, 66251208440),  # 55s with logging commented out; 9.5GB memory (59.4% of 1GGB)
            # TestCase(10**8, UNKNOWN),
            # TestCase(10**9, UNKNOWN),
            # TestCase(10**10, UNKNOWN),
            # TestCase(10**11, UNKNOWN),
            # TestCase(10**12, UNKNOWN),
            # TestCase(10**13, UNKNOWN),
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
    # logDebug(f"get_fib_up_to_n({n})")
    while (f := sum(fib[-2:])) and f <= n:
        fib.append(f)
        # logDebug(f"  {f}: {fib}")
    # logDebug(f"get_fib_up_to_n({n}) has {len(fib)} elements")
    # logDebug("")
    return fib

def not_zeckendorf(n):
    fib = get_fib_up_to_n(n)
    counts = defaultdict(int)
    counts[0] = 1
    for f in fib:
        # logDebug(f"{f} (start of this round)")
        for s, c in sorted(counts.items()):
            t = s+f
            # logDebug(f"  {s}={c}         (existing)")
            # logDebug(f"    {t}={counts[t]} (existing)")
            if t <= n:
                counts[t] += c
                # logDebug(f"    {t}={counts[t]} (incremented)")
        # logDebug(f"  {sorted(counts.items())}")
        # logDebug(f"{f} (end of this round)")
        # for s, c in sorted(counts.items()):
        #    if s > n:
        #        continue
        #    # logDebug(f"  {s}: {c}")
    total = sum(c for s, c in counts.items() if s <= n)
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
