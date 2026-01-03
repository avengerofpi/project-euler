#!/usr/bin/env python3

# Imports
from datetime import timedelta
from pathlib import Path
import time
from math import prod

# Constants
N = 1 * 1000 * 1000 * 1000
root_dir = Path(__file__).parent

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

def computePrimesUpToN2(N):
    """
    Trying to write a more efficient prime generator by avoiding checking
    against small primes. This is referred to as the 'wheel method' as you sort
    of roll a "wheel" that step over any number that is a multiple of thos
    small primes. For the case where you want to avoid checking [2, 3, 5],
    you have
      wheel = (1, 7, 11, 13, 17, 19, 23, 29)
    Those are the numbers less than
        lcm(2,3,5) = 2 * 3 * 5 = 30
    that are relatively prime to 2, 3, and 5. So if you limit yourself to
    checking number of the form
        n = 30*k + b for k >= 0 and b in `wheel`
    you do are guaranteed to be coprime to 2, 3, 5 and thus do not need to
    check those for any such value n.
    """
    primes = []
    basis = [2, 3, 5]
    maxBasis = max(basis)

    # Add basis to primes
    for n in basis:
        if n <= N:
            primes.append(n)
            logInfo(f"{n}")

    # Setup wheel
    if N >= maxBasis:
        wheelSize = prod(basis)
        wheelNodes = tuple(i for i in range(1, wheelSize) if all(i % basisEntry != 0 for basisEntry in basis))
        logVerbose(f"Wheel size: {wheelSize}")
        logVerbose(f"Wheel nodes: {wheelNodes}")
        for node in wheelNodes:
            if node <= N:
                primes.append(node)
                logInfo(f"{node}")

    #
    iterNum = 1
    cursor = wheelSize
    minPrimeIndexToCheck = len(basis)
    checkPrimesI = 0
    while cursor < N:
        for node in wheelNodes:
            candidateP = cursor + node
            while ((checkPrimesI < len(primes) - 1) and (primes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in primes[minPrimeIndexToCheck :checkPrimesI + 1]):
                primes.append(candidateP)
                logInfo(f"{candidateP}")
        iterNum += 1
        cursor += wheelSize
    return tuple(primes)


def primes_up_to_10k():
    return _primes_from_file(f"{root_dir}/primes-up-to-10000.txt")

def primes_up_to_1m():
    return _primes_from_file(f"{root_dir}/primes-up-to-1million.txt")

def primes_up_to_20m():
    return _primes_from_file(f"{root_dir}/primes-up-to-20million.txt")

def primes_up_to_100m():
    return _primes_from_file(f"{root_dir}/primes-up-to-100million.txt")

def primes_up_to_1b():
    return _primes_from_file(f"{root_dir}/primes-up-to-1billion.txt")

def _primes_from_file(filename):
    with open(filename, "r") as f:
        primes = []
        while line := f.readline():
            primes.append(int(line))
    return primes

# Main logic
functions = [
    { 'f': computePrimesUpToN,  'name': "computePrimesUpToN" },
    { 'f': computePrimesUpToN2, 'name': "computePrimesUpToN2" },
]
def main():
    powersOf10 = [4, 5, 6, 7, 8]
    powersOf10 = [4, 5, 6]
    powersOf10 = [4]
    for ff in functions:
        f = ff['f']
        fName = ff['name']
        logDebug(f"Checking times for '{fName}'")
        for i in powersOf10:
            N = 10 ** i
            startTime = getTimeInMillis()
            primes = f(N)
            endTime = getTimeInMillis()
            logTimeDiff = endTime - startTime
            logDebug(f"  Time spent computing {len(primes):9} <= {N:12} = 10 ** {i:2} -> {timedelta(milliseconds=logTimeDiff)}")
        logDebug()

if __name__ == "__main__":
    main()
