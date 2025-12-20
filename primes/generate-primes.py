#!/usr/bin/env python3

# Imports
from datetime import timedelta
import time

# Constants
N = 1 * 1000 * 1000 * 1000

# Logging
info = False
debug = True
verbose = False
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)

# Functions
def getTimeInMillis():
    return int(time.time() * 1000)

def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as a numerically-sorted tuple.

    This is a simple seive generator, nothing fancy.
    """
    primes = []
    checkPrimesI = 0
    if N >= 2:
        primes.append(2)
        for candidateP in range(3, N+1, 2):
            while ((checkPrimesI < len(primes) - 1) and (primes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in primes[0:checkPrimesI + 1]):
                primes.append(candidateP)
                logInfo(f"{candidateP}")
    return tuple(primes)

# Main logic
def main():
    powersOf10 = [4, 5, 6, 7, 8]
    for i in powersOf10:
        N = 10 ** i
        startTime = getTimeInMillis()
        primes = computePrimesUpToN(N)
        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logDebug(f"Time spent computing {len(primes):9} <= {N:12} = 10 ** {i:2} -> {timedelta(milliseconds=logTimeDiff)}")

if __name__ == "__main__":
    main()
