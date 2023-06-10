#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict

# Constants
debug = True
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(40, "6.799056"),
    TestCase(2800, "715.019337"),
    TestCase(10 ** 6, "UNKNOWN"),
]

# Functions
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)

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
                #print(f"{candidateP}")
    return tuple(primes)

def filterByUnitsDigitAndSort(arr, digit):
    return sorted(n for n in arr if n % 10 == digit)

def getPrimesToInclude(primesA, primesB, N):
    modA = primesA[0] % 10
    width = int(log10(sqrt(N))) + 1

    logDebug(f"Checking primes ending in {modA}:")
    pAsToInclude = list()
    pAsToIncludeDict = dict()
    for pA in primesA:
        primesBCofactors = []
        for pB in primesB:
            if (pB > pA) and (pA * pB <= N):
                primesBCofactors.append(pB)
        if len(primesBCofactors) > 0:
            msg = f"  {pA:{width}} (because of "
            termsStart = 4
            termsEnd = 2
            if len(primesBCofactors) > termsStart + termsEnd:
                primesBprefix = primesBCofactors[0:termsStart]
                primesBsuffix = primesBCofactors[-termsEnd:]
                msg += f"{primesBprefix} ... {primesBsuffix}"
            else:
                msg += f"{primesBCofactors}"
            msg += f" ({len(primesBCofactors)}))"
            logDebug(msg)

            pAsToInclude.append(pA)
            pAsToIncludeDict[pA] = tuple(primesBCofactors)

    # Collecting map of pBs cofactors lists to pAs that satisfy/pair with them
    cofactorsListToPAsDict = defaultdict(list)
    for pA in pAsToIncludeDict.keys():
        cofactors = pAsToIncludeDict[pA]
        cofactorsListToPAsDict[cofactors].append(pA)
    # Now figuring out which pAs to include, and which to replace with pB cofactors
    for cofactors in cofactorsListToPAsDict.keys():
        pAsList = cofactorsListToPAsDict[cofactors]
        if prod(cofactors) < prod(pAsList):
            logDebug(f"  {pAsList} can be removed and replaced with {cofactors}")
            for pA in pAsList:
                pAsToInclude.remove(pA)
            pAsToInclude.extend(cofactors)
            
    return pAsToInclude

# Main logic
def main():
    #for N in (40, 2800, 10 ** 6):
    #for N in (40, 2800):
    for test in TESTS:
        #N = 40
        N = test.N
        expected = test.expected
        logDebug(f"Running against N = {N}")

        primesUpToN = computePrimesUpToN(N)
        p3s = filterByUnitsDigitAndSort(primesUpToN, 3)
        p7s = filterByUnitsDigitAndSort(primesUpToN, 7)
        p9s = filterByUnitsDigitAndSort(primesUpToN, 9)

        # All primes ending in 3 need to be factors
        valuesToMultiply = sorted(p3s)

        # All remaining factors end in either 7 or 9. In order for a prime `p7`
        # that ends in 7 to be included, it is necessary and sufficient for
        # there to be larger prime `p9` that ends in 9 satisfying
        #   p7 * p9 <= N.
        # Similarly, in order for a prime `p9` that ends in 9 to be included,
        # it is necessary and sufficient for there to be larger prime `p7` that
        # ends in 7 satisfying
        #   p7 * p9 <= N.
        p7sToInclude = getPrimesToInclude(p7s, p9s, N)
        p9sToInclude = getPrimesToInclude(p9s, p7s, N)
        logDebug(f"p7sToInclude: {p7sToInclude}")
        logDebug(f"p9sToInclude: {p9sToInclude}")

        if len(p7sToInclude) > 0 and len(p9sToInclude) > 0:
            maxP7 = max(p7sToInclude)
            maxP9 = max(p9sToInclude)
            p7sToNotInclude = set()
            p9sToNotInclude = set()

            for p7 in p7sToInclude:
                if p7 not in p7sToNotInclude:
                    valuesToMultiply.append(p7)
            for p9 in p9sToInclude:
                if p9 not in p9sToNotInclude:
                    valuesToMultiply.append(p9)

        product = prod(valuesToMultiply)
        ans = log(product)
        ansStr = f"{ans:.6f}"
        successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
        print(f"{N}: {ansStr} - {successStr}")
        logDebug()

# Main logic
if __name__ == '__main__':
    main()
