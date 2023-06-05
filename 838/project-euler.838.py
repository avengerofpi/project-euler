#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt

# Constants
debug = True
class Test:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    Test(40, "6.799056"),
    Test(1080, "UNKNOWN"),
    Test(2190, "UNKNOWN"),
    Test(2800, "715.019337"),
]
    


# Functions
def logDebug(msg = ""):
    if debug:
        print(msg)

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
    pAsToInclude = set()
    for iA in range(len(primesA)):
        pA = primesA[iA]
        primesBCofactors = []
        for iB in range(len(primesB)):
            pB = primesB[iB]
            if pB > pA:
                if pA * pB <= N:
                    pAsToInclude.add(pA)
                    primesBCofactors.append(pB)
                    #logDebug(f"  {pA} (because of {pB} ({pA * pB}))")
                # only need to check the smallest such pB for each pA
                #break
        if len(primesBCofactors) > 0:
            logDebug(f"  {pA:{width}} (because of {primesBCofactors})")
            #logDebug()
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

        if len(p7sToInclude) > 0 and len(p9sToInclude) > 0:
            maxP7 = max(p7sToInclude)
            maxP9 = max(p9sToInclude)
            p7sToNotInclude = set()
            p9sToNotInclude = set()
            if maxP7 > maxP9:
                for p7 in p7sToInclude:
                    if p7 > maxP9:
                        logDebug(f"  removing {p7}")
                        p7sToNotInclude.add(p7)
            else:
                for p9 in p9sToInclude:
                    if p9 > maxP7:
                        logDebug(f"  removing {p9}")
                        p9sToNotInclude.add(p9)

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
