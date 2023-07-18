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
    def __init__(self, base, exponent, expected):
        self.base = base
        self.exponent = exponent
        self.expected = expected

UNKNOWN = "UNKNOWN"
TESTS = [
TestCase(800, 1, 2),
TestCase(800, 800, 10790),
TestCase(800800, 800800, UNKNOWN),
]

# Logging 
info = True
debug = False
verbose = False
verbosePrimes = False
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
def logVerbosePrimes(msg = ""):
    if verbosePrimes:
        print(msg, flush=True)
def logTiming(msg = ""):
    if timing:
        print(msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def computePrimesWithHybridIntegerConstraint(logN):
    """
    Inefficiently determine all primes p such that
        2**p * p**2 <= logN
    returning the collection as some collection object.
    Collecting the primes satisfying this constraint ensures that we can quickly determine the sets of primes
        {p, q}
    such that
        p**q * q**p <= logN
    This is a simple seive generator, nothing fancy.
    """
    logVerbosePrimes(f"Computing primes p such that 2**p * p**2 <= {logN}")
    primesWithLogs = []
    checkPrimesI = 0
    logTwo = log(2)
    # min bound should be log(16)
    minBound = log(hybridPower(2, 2, logTwo, logTwo))
    #logVerbosePrimes(f"Min bound is {minBound}")
    if logN >= minBound:
        primesWithLogs.append((2, logTwo))
        candidateP = 3
        logCandidateP = log(candidateP)
        while hybridPower(2, candidateP, logTwo, logCandidateP) <= logN:
            while ((checkPrimesI < len(primesWithLogs) - 1) and (primesWithLogs[checkPrimesI + 1][0] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for (p,logP) in primesWithLogs[0:checkPrimesI + 1]):
                primesWithLogs.append((candidateP, logCandidateP))
                #logVerbosePrimes(f"  {candidateP}")
            candidateP += 2
            logCandidateP = log(candidateP)
    
    logVerbosePrimes(f"Found {len(primesWithLogs)} primes from {primesWithLogs[0][0]} to {primesWithLogs[-1][0]}")
    return primesWithLogs

def hybridPower(p, q, logP = None, logQ = None):
    if not logP:
        logP = log(p)
    if not logQ:
        logQ = log(q)
    return (q * logP) + (p * logQ)

def printTestResult(tc, result):
    PATH_COLOR = Fore.RED
    RESET_COLOR = Style.RESET_ALL

    base = tc.base
    exponent = tc.exponent
    logN = exponent*log(base)

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
    logInfo(f"{c}{b} Result for {logN}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")

def runTest(test):
    startTime = getTimeInMillis()
    
    base = test.base
    exponent = test.exponent
    logN = exponent*log(base)

    expected = test.expected

    logInfo(f"Running against log(N) = {logN}")
    primesWithLogs = computePrimesWithHybridIntegerConstraint(logN)

    logInfo(f"{len(primesWithLogs)} primes")
    logInfo(f"Max prime: {max(primesWithLogs)[0]}")

    numPrimes = len(primesWithLogs)
    maxIndex = numPrimes - 1
    count = 0
    for i in range(numPrimes):
        p, logP = primesWithLogs[i]
        for j in range(maxIndex, i, -1):
            q, logQ = primesWithLogs[j]
            if hybridPower(p, q, logP, logQ) <= logN:
                logDebug(f"Valid pair ({p}, {q})")
                # done, we have found the largest value we can use
                maxIndex = j
                increment = j - i
                count += increment
                break

    ans = count

    result = TestCase(base, exponent, ans)
    printTestResult(test, result)

    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

    logInfo(f"{'-' * 60}")
    logInfo("")

# Main logic
def main():
    for test in TESTS:
        runTest(test)

# Main logic
if __name__ == '__main__':
    main()
