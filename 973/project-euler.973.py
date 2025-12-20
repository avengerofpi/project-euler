#!/usr/bin/env python3

# Imports
from collections import defaultdict
import scipy
import numpy as np
from numpy import add, array
from datetime import timedelta
import time
from colorama import Fore, Back, Style
from copy import deepcopy
from fractions import Fraction
from math import log10

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
            TestCase(5, 42),
            TestCase(6, 58),
            TestCase(7, 206),
            TestCase(8, 326),
            TestCase(9, 946),
            TestCase(10, 1418),
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

# Constants
MOD = 10**9 + 7

# Logging
info = False
debug = False
verbose = False
timing = False
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

    ISSUE: This method is computing the "partitions of n." The size of such
    set is called the "partition function of n," and it grows too fast to be usable
    much beyond n = 30. According to
        https://en.wikipedia.org/wiki/Partition_function_(number_theory)
        https://oeis.org/A000041
    the size of the set for n = 10**4 is about 3.6 * 10**106.

    So I need to find a better solution than merely trying to iterate through this
    "just once." Hmm...
    """
    # logDebug(f"generate_pile_sizes({n})")
    sizes = [n]
    while sizes:
        # logDebug(f"  {sizes}")
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
    # logDebug(f"    redistribute_pile({sizes}, {i})")
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

        # logDebug(f"      {redistribution}")
        redistributions.append(tuple(redistribution))

    return redistributions

def runRandomDealings(n):
    logInfo(f"Computing X({n}):")

    x = 0
    xmap = defaultdict(lambda: defaultdict(Fraction))

    pile_sizes = list(generate_pile_sizes(n))
    logInfo(f"generate_pile_sizes({n}) has size {len(pile_sizes)}")
    logInfo(f"Computing equation maps")
    for sizes in pile_sizes:
        k = len(sizes)
        for i in range(k):
            for redistribution in redistribute_pile(sizes, i):
                xmap[sizes][redistribution] += 1

        denominator = k * (k-1)
        for redistribution, numerator in reversed(xmap[sizes].items()):
            xmap[sizes][redistribution] = Fraction(numerator, denominator)

    print(f"xmap:")
    for sizes in xmap:
        score = score_piles(sizes)
        print(f"  e({sizes}) = {score} + ", end="")
        for redistribution, coef in reversed(xmap[sizes].items()):
            print(f"{coef}*e{redistribution} + ", end="")
        print("")

    # Form equation and solve
    logInfo(f"Computing matrix and array")
    matrix = []
    for sizes, redistributions in xmap.items():
        row = [-redistributions[s] for s in pile_sizes] + [Fraction(score_piles(sizes))]
        row[pile_sizes.index(sizes)] += 1
        matrix.append(row)

    # Perform Gaussian elimination
    A = matrix
    num_rows = len(A)
    num_cols = len(A[0])
    from itertools import product
    print("A:")
    printFractionsMatrix(A)
    for i in range(num_rows):
        # Make the diagonal contain all 1s
        A[i] = [e / A[i][i] for e in A[i]]
        for j in range(i + 1, num_rows):
            A[j] = [A[j][k] - A[j][i] * A[i][k] for k in range(num_cols)]

    # Back substitution to find the solution
    print("X:")
    X = [0] * num_rows
    for i in range(num_rows - 1, -1, -1):
        X[i] = A[i][-1] - sum(A[i][i + 1:num_rows][k] * X[i + 1:num_rows][k] for k in range(num_rows-i-2))
        print(f"  {X[i]}")

    x = round(X[-1])
    print(f"X({n}) = {x} = {x % MOD} % {MOD}")
    print()

    logInfo(f"------------------- RESULT DETAILS -------------------")
    logInfo(f"  X({n}) = {x} = {x % MOD} % {MOD}")
    logInfo(f"------------------------------------------------------")

    if verbose:
        pass

    return x

def printFractionsMatrix(m):
    for row in m:
        print(f"[{', '.join(map(str, row))}]")

def computePartitionNumber(n):
    # p((a,b)) is the number of partitions of a where the min partition size is b
    # e.g., p(7,2) = |{(5,2), (3,2,2)}| = 2
    p = [[0] * (n+1) for i in range(n+1)]
    p[0][1] = 1
    pn =  [1] # partition number of n
    for i in range(1, n+1):
        for j in range(1, i):
            p[i][j] = sum(p[i-j][j:])
        p[i][i] = 1
        pn.append(sum(p[i]))
        print(f"pn({i}) = {pn[i]} = {pn[i]:e}")

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

    computePartitionNumber(30)

# Main logic
if __name__ == '__main__':
    main()
