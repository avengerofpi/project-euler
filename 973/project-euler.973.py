#!/usr/bin/python3

# Imports
from collections import defaultdict
import scipy
import numpy
from numpy import add, array
from datetime import timedelta
import time
from colorama import Fore, Back, Style
from copy import deepcopy
from fractions import Fraction

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
            TestCase(2, 2),
            TestCase(3, 10),
            TestCase(4, 14),
            TestCase(5, UNKNOWN),
            # TestCase(6, UNKNOWN),
            # TestCase(7, UNKNOWN),
            # TestCase(8, UNKNOWN),
            # TestCase(9, UNKNOWN),
            # TestCase(10, 1418),
        ]
        self.CHALLENGES = []

# Constants
MOD = 10**9 + 7

# Logging
info = True
debug = True
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
    if ans == expected:
        successStr = "SUCCESS"
        b = Back.GREEN
        c = Fore.RED
    else:
        successStr = f"FAILURE (expected {expected} but got {ans})"
        b = Back.RED
        c = Fore.YELLOW
    logInfo(f"{c}{b} Result for {tc.n}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")
    logInfo(f"{c}{b}TestCase({tc.n}, {result.expected}),{RESET_COLOR}")

def score_piles(pile_sizes):
    return reduce(xor, pile_sizes)

def generate_pile_sizes(n):
    """Generator for all piles sizes possible for a deck of size n.
    
    Start with (n), (n-1,1), (n-2,2), (n-2,1,1), ...
    """
    # breakpoint()
    logDebug(f"generate_pile_sizes({n})")
    sizes = [n]
    while sizes:
        logDebug(f"  {sizes}")
        yield tuple(sizes)
        if sizes[0] == 1:
            break

        i = len(sizes) - 1
        while sizes[i] == 1:
            i -= 1
        i_size = sizes[i]
        i_size_new = i_size - 1

        new_sizes = sizes[0:i]
        remainder_to_redistribute = n - sum(new_sizes)
        new_sizes.extend([i_size_new] * (remainder_to_redistribute // i_size_new))
        final_remainder = n - sum(new_sizes)
        if final_remainder:
            new_sizes.append(final_remainder)

        assert min(new_sizes) > 0 and sum(sizes) == n

        sizes = new_sizes


def redistribute_pile(sizes, i):
    """Return an iterable of sizes derived from redistributing pile at index i.

    E.g., sizes=(3,2,1) and i=2 would be [(4,1,1), (3,2,1)]
    """
    logDebug(f"    redistribute_pile({sizes}, {i})")
    v = sizes[i]
    redistributions = []
    for j in range(len(sizes)):
        redistribution = list(sizes)
        if j == i:
            continue

        redistribution[j] += 1
        if v > 1:
            redistribution.extend([1] * (v-1))

        redistribution = sorted(redistribution[:i] + redistribution[i+1:])
        redistribution.reverse()

        logDebug(f"      {redistribution}")
        redistributions.append(tuple(redistribution))

    return redistributions

def runRandomDealings(n):
    logInfo(f"Computing X({n}):")

    x = 0
    xmap = defaultdict(lambda: defaultdict(int))

    pile_sizes = list(generate_pile_sizes(n))
    for sizes in pile_sizes:
        k = len(sizes)
        for i in range(k):
            for redistribution in redistribute_pile(sizes, i):
                xmap[sizes][redistribution] += 1

        denominator = k * (k-1)
        for redistribution, numerator in reversed(xmap[sizes].items()):
            xmap[sizes][redistribution] = Fraction(numerator, denominator)

        

    print(f"xmap:")
    for sizes in reversed(xmap):
        score = score_piles(sizes)
        print(f"  e({sizes}) = {score} + ", end="")
        for redistribution, coef in reversed(xmap[sizes].items()):
            print(f"{coef}*e{redistribution} + ", end="")
        print("")

    import numpy as np
    # a = np.array([[1, 2], [3, 5]])
    # b = np.array([1, 2])
    # x = np.linalg.solve(a, b)
    # x

    matrix = []
    scores = []
    for sizes, redistributions in reversed(xmap.items()):
        matrix.append([redistributions[s] or Fraction(0,1) for s in pile_sizes])
        scores.append(Fraction(score_piles(sizes), 1))
    a = np.array(matrix)
    b = np.array(scores)
    print(f"a: {a}")
    print(f"b: {b}")
    x = np.linalg.solve(a, b)

    logInfo(f"------------------- RESULT DETAILS -------------------")
    logInfo(f"  X({n}) = {x} = {x % MOD} % {MOD}")
    logInfo(f"------------------------------------------------------")

    if verbose:
        pass

    return x

def runTests(tests):
    for test in tests:
        startTime = getTimeInMillis()
        n = test.n
        logInfo(f"Running against n = {n}")

        ansBeforeMod = runRandomDealings(n)
        ans = ansBeforeMod % MOD
        result = TestCase(n, ans)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()
        logInfo()
        logInfo()

def troubleshoot():
    for n in range(3, 10):
        ansBeforeMod = runRandomDealings(n)
        ans = ansBeforeMod % MOD
        logInfo(f"X({n:4d}) = {ansBeforeMod:20d} = {ans:10d} mod {MOD}")
        logInfo(f"TestCase({n}, {ans})")

# Main logic
def main():
    #troubleshoot()

    testCaseCollections = TestCaseCollections()
    tests = testCaseCollections.BASE
    runTests(tests)

# Main logic
if __name__ == '__main__':
    main()
