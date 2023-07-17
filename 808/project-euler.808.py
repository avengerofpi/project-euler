#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict
from datetime import timedelta
import time

# Constants
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

UNKNOWN = "UNKNOWN"
TESTS = [
TestCase(10, 15633754),
TestCase(20, 4116550636820),
TestCase(50, UNKNOWN),
]

# Logging 
info = True
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

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as some collection object.
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
    return tuple(primes)

def getPrimes():
    #filename = "../primes/primes-up-to-10000.txt"
    #filename = "../primes/primes-up-to-1million.txt"
    #filename = "../primes/primes-up-to-20million.txt"
    filename = "../primes/primes-up-to-100million.txt"
    #filename = "../primes/primes-up-to-1billion.txt"

    with open(filename) as f:
        return [int(line) for line in f.readlines()]
    """
    validStartsAndStops = ['1', '9']
    with open(filename) as f:
        while not f.closed:
            try:
                p = int(f.readline())
            except:
                # handle end of file
                break
            p2 = p**2

            p2list = list(str(p2))
            p2listRev = reversed(p2list)
            if p2listRev == p2list:
                logDebug(f"Skipping {p} -> {p2} (palindrome)")
                continue
            if p2list[0] not in validStartsAndStops:
                logDebug(f"Skipping {p} -> {p2} (first char must be in {validStartsAndStops})")
                continue
            if p2list[-1] not in validStartsAndStops:
                logDebug(f"Skipping {p} -> {p2} (last char must be in {validStartsAndStops})")
                continue

            p2rev = int("".join(p2listRev))
            pRev = int(sqrt(p2rev))
            if pRev**2 != p2rev:
                logInfo(f"Error: working with values that may be too large for math.sqrt to be accurate enough")
                logInfo(f"  {p2Rev} --(sqrt)--> {pRev} --(squared)--> {pRev**2} != {p2rev}")
                break
    """

def runTest(test):
    startTime = getTimeInMillis()
    
    N = test.N
    expected = test.expected

    logInfo(f"Running against N = {N}")

    #primes = computePrimesUpToN(10**7)
    primes = set(getPrimes())
    logInfo(f"{len(primes)} primes")
    logInfo(f"Max prime: {max(primes)}")

    validStartsAndStops = ['1', '9']

    revSquarePrimes = set()
    basePrimes = set()
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
        #if pRev**2 != p2rev:
        #    logInfo(f"Error: working with values that may be too large for math.sqrt to be accurate enough")
        #    logInfo(f"  {p} -> {p2} -> {p2rev} --(sqrt)--> {pRev} --(squared)--> {pRev**2} != {p2rev}")
        #    break

        forwardSquares.add(p2)
        reverseSquares.add(p2rev)

        """
        if pRev in primes:
            logDebug(f"  {p:7} -> {p2:15} -> {p2rev:15} --(sqrt)--> {pRev:7} --(squared)--> {pRev**2:15}")
            revSquarePrimes.add(p2)
            revSquarePrimes.add(p2rev)
            basePrimes.add(p)
            basePrimes.add(pRev)
        """

    revSquarePrimes = forwardSquares.intersection(reverseSquares)

    numRevSquarePrimes = len(revSquarePrimes)
    logInfo(f"Num rev square primes: {numRevSquarePrimes}")
    for p in sorted(revSquarePrimes):
        logInfo(f"  {p}")
    for p in sorted(basePrimes):
        p2 = p**2
        if p2 in revSquarePrimes:
            logDebug(f"  {p:7} -> {p**2:15}")
    if numRevSquarePrimes >= N:
        ans = sum(sorted(revSquarePrimes)[0:N])
    else:
        ans = f"Did not find enough reverse square primes. Need {N} but only found {numRevSquarePrimes}"

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
    #getPrimesUpToOneBillion()
    #return

    for test in TESTS:
        runTest(test)


# Main logic
if __name__ == '__main__':
    main()
