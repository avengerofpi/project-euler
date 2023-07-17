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
from colorama import Fore, Back, Style
from copy import deepcopy
#print(f"{Fore.GREEN}hello{Fore.RED}World{ansi.Style.RESET_ALL}")

# Constants
class TestCase:
    def __init__(self, N, expected, primeBound, primesFilename = None):
        self.N = N
        self.expected = expected
        self.primeBound = primeBound
        self.primesFilename = primesFilename

UNKNOWN = "UNKNOWN"
TESTS = [
TestCase(10, 15633754, 10**4),
TestCase(20, 4116550636820, 10**7),
TestCase(50, UNKNOWN, None, "../primes/primes-up-to-100million.txt"),
]

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
def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as some collection object.
    This is a simple seive generator, nothing fancy.
    """
    logDebug(f"Computing primes up to {N}")
    primes = []
    checkPrimesI = 0
    if N >= 2:
        primes.append(2)
        for candidateP in range(3, N+1, 2):
            while ((checkPrimesI < len(primes) - 1) and (primes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in primes[0:checkPrimesI + 1]):
                primes.append(candidateP)
    logDebug(f"Computing primes up to {N} - found {len(primes)} from {primes[0]} to {primes[-1]}")
    return primes

def getPrimesFromFile(filename):
    logDebug(f"Getting primes from file: '{filename}'")
    #filename = "../primes/primes-up-to-10000.txt"
    #filename = "../primes/primes-up-to-1million.txt"
    #filename = "../primes/primes-up-to-20million.txt"
    #filename = "../primes/primes-up-to-100million.txt"

    with open(filename) as f:
        return [int(line) for line in f.readlines()]

def printTestResult(tc, result):
    PATH_COLOR = Fore.RED
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
    logInfo(f"{c}{b} Result for {tc.N}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")

def runTest(test):
    startTime = getTimeInMillis()
    
    N = test.N
    expected = test.expected
    primeBound = test.primeBound
    primesFilename = test.primesFilename

    logInfo(f"Running against N = {N}")

    if primesFilename:
        primes = getPrimesFromFile(primesFilename)
    elif primeBound:
        primes = computePrimesUpToN(primeBound)
    else:
        logInfo("ERROR: Neither primeBound ({primeBound}) nor primesFilename ({primesFilename}) is valid. Cannot determine list of prime to work with.")
        primes = []

    primes = set(primes)

    logInfo(f"{len(primes)} primes")
    logInfo(f"Max prime: {max(primes)}")

    validStartsAndStops = ['1', '9']

    forwardSquares = set()
    reverseSquares = set()
    for p in sorted(primes):
        p2 = p**2

        p2list = list(str(p2))
        p2listRev = list(reversed(p2list))
        if p2listRev == p2list:
            logVerbose(f"Skipping {p} -> {p2} (palindrome)")
            continue
        if p2list[0] not in validStartsAndStops:
            logVerbose(f"Skipping {p} -> {p2} (first char must be in {validStartsAndStops})")
            continue
        if p2list[-1] not in validStartsAndStops:
            logVerbose(f"Skipping {p} -> {p2} (last char must be in {validStartsAndStops})")
            continue

        p2rev = int("".join(p2listRev))
        pRev = int(sqrt(p2rev) + 0.5)

        forwardSquares.add(p2)
        reverseSquares.add(p2rev)

    revSquarePrimes = forwardSquares.intersection(reverseSquares)

    numRevSquarePrimes = len(revSquarePrimes)
    logInfo(f"Num rev square primes: {numRevSquarePrimes}")
    for p in sorted(revSquarePrimes):
        logInfo(f"  {p}")
    if numRevSquarePrimes >= N:
        ans = sum(sorted(revSquarePrimes)[0:N])
    else:
        ans = f"Did not find enough reverse square primes. Need {N} but only found {numRevSquarePrimes}"

    result = TestCase(N, ans, None)
    printTestResult(test, result)

    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

    logInfo(f"{'-' * 60}")
    logInfo(f"Ans: {ans}")

    """
    primeSquares = [p**2 for p in primes]
    primeSquaresNonPalindromes = [p2 for p2 in primeSquares if str(p2) != "".join(reversed(list(str(p2))))]
    primeSquaresNonPalindromesReversible = [p2 for p2 in primeSquaresNonPalindromes if int("".join(reversed(list(str(p2))))) in primeSquaresNonPalindromes]
    #primeSquaresPalindromes = [p2 for p2 in primeSquares if str(p2) == "".join(reversed(list(str(p2))))]
    #logInfo(primeSquaresPalindromes)
    logInfo(len(primeSquaresNonPalindromesReversible))
    #logInfo(primeSquaresNonPalindromesReversible)
    return

    for p in primes:
        p2 = p**2
        p2a = str(p2)

    #for p in primes:
    """

    logInfo("")

# Main logic
def main():
    for test in TESTS:
        runTest(test)


# Main logic
if __name__ == '__main__':
    main()
